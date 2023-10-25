"""
MIT License

Copyright (c) 2020-present phenom4n4n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import textwrap
from difflib import SequenceMatcher
from functools import partial
from io import BytesIO
from typing import Tuple

import aiohttp
import discord
import kuroutils
from PIL import Image, ImageDraw, ImageFont
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path


class TypeRacer(kuroutils.Cog):
    """
    Race to see who can type the fastest!

    Credits to Cats3153.
    """

    __author__ = ["PhenoM4n4n", "Kuro"]
    __version__ = "1.0.4"

    def __init__(self, bot: Red):
        super().__init__(bot)
        self.session = aiohttp.ClientSession()
        self._font = None

    async def cog_unload(self) -> None:
        await self.session.close()

    @property
    def font(self) -> ImageFont:
        if self._font is None:
            self._font = ImageFont.truetype(
                f"{bundled_data_path(self)}/Menlo.ttf", size=30, encoding="unic"
            )
        return self._font

    @commands.hybrid_command(aliases=["typeracer"])
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def typerace(self, ctx: commands.Context) -> None:
        """Begin a typing race!"""
        try:
            quote, author = await self.get_quote()
        except KeyError:
            await ctx.send("Could not fetch quote. Please try again later.")
            return

        color = discord.Color.random()
        img = await self.render_typerace(quote, color)
        embed = discord.Embed(color=color)
        embed.set_image(url="attachment://typerace.png")
        if author:
            embed.set_footer(text=f"~ {author}")

        message = await ctx.send(file=discord.File(img, "typerace.png"), embed=embed)
        acc = 0.0

        def check(message: discord.Message) -> bool:
            if message.channel != ctx.channel or message.author.bot or not message.content:
                return False
            content = " ".join(message.content.split())  # remove duplicate spaces
            accuracy = SequenceMatcher(None, quote, content).ratio()

            if accuracy >= 0.95:
                nonlocal acc
                acc = accuracy * 100
                return True
            return False

        view = discord.ui.View()
        button = discord.ui.Button(
            style=discord.ButtonStyle.link, label="Jump to Message", url=message.jump_url
        )
        view.add_item(button)
        try:
            winner = await self.bot.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                color=discord.Color.blurple(),
                description=f"No one typed the sentence in time.",
            )
            await ctx.send(
                embed=embed, reference=message.to_reference(fail_if_not_exists=False), view=view
            )
            return

        seconds = (winner.created_at - message.created_at).total_seconds()
        winner_reference = winner.to_reference(fail_if_not_exists=False)
        wpm = (len(quote) / 5) / (seconds / 60) * (acc / 100)
        description = (
            f"{winner.author.mention} typed the sentence in `{seconds:.2f}s` "
            f"with **{acc:.2f}%** accuracy. (**{wpm:.1f} WPM**)"
        )
        embed = discord.Embed(color=winner.author.color, description=description)
        await ctx.send(embed=embed, reference=winner_reference, view=view)

    async def get_quote(self) -> Tuple[str, str]:
        async with self.session.get("https://api.quotable.io/random") as resp:
            data = await resp.json()
        return data["content"], data["author"]
        # Backup API just in case the one above goes down
        # async with self.session.get("https://zenquotes.io/api/random") as resp:
        #    data = await resp.json(content_type=None)[0]
        # return data["q"], data["a"]

    def generate_image(self, text: str, color: discord.Color) -> discord.File:
        margin = 40
        newline = 30 // 5

        wrapped = textwrap.wrap(text, width=35)
        text = "\n".join(line.strip() for line in wrapped)

        img_width = self.font.getsize(max(wrapped, key=len))[0] + 2 * margin
        img_height = 30 * len(wrapped) + (len(wrapped) - 1) * newline + 2 * margin

        with Image.new("RGBA", (img_width, img_height)) as im:
            draw = ImageDraw.Draw(im)
            draw.multiline_text(
                (margin, margin), text, spacing=newline, font=self.font, fill=color.to_rgb()
            )

            buffer = BytesIO()
            im.save(buffer, "PNG")
            buffer.seek(0)

        return buffer

    async def render_typerace(self, text: str, color: discord.Color) -> discord.File:
        func = partial(self.generate_image, text, color)
        task = self.bot.loop.run_in_executor(None, func)
        try:
            return await asyncio.wait_for(task, timeout=60)
        except asyncio.TimeoutError:
            raise commands.UserFeedbackCheckFailure(
                "An error occurred while generating this image. Try again later."
            )
