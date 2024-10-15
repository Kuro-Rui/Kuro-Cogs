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
import functools
import math
import textwrap
from difflib import SequenceMatcher
from io import BytesIO
from typing import Dict, List, Optional, Tuple

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
    __version__ = "1.1.3"

    def __init__(self, bot: Red):
        super().__init__(bot)
        self.session = aiohttp.ClientSession()
        self.sessions: Dict[int, dict] = {}
        self._font = None

    async def cog_unload(self) -> None:
        super().cog_unload()
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
    async def typerace(self, ctx: commands.Context, winners: commands.Range[int, 1, 10] = 1):
        """Start a typing race!"""
        try:
            quote, author = await self.get_quote()
        except KeyError:
            await ctx.send("Could not fetch quote. Please try again later.")
            return
        words = quote.split()
        word_length = math.ceil(sum(len(word) for word in words) / len(words))
        color = discord.Color.random()
        fp = await self.render_typerace(quote, color)
        embed = discord.Embed(color=color)
        embed.set_image(url="attachment://typerace.png")
        if author:
            embed.set_footer(text=f"~ {author}")
        start = await ctx.send(file=discord.File(fp, "typerace.png"), embed=embed)

        winners_cache: List[discord.Member] = []
        messages: List[Tuple[discord.Message, float, float, float]] = []

        def check(message: discord.Message) -> bool:
            if message.channel != ctx.channel or message.author.bot or not message.content:
                return False
            if message.author in winners_cache:
                return False
            content = " ".join(message.content.split())  # remove duplicate spaces
            accuracy = SequenceMatcher(None, quote, content).ratio()
            if accuracy < 0.95:
                return False
            winners_cache.append(message.author)
            seconds = (message.created_at - start.created_at).total_seconds()
            wpm = (len(quote) * accuracy / word_length) / (seconds / 60)
            messages.append((message, seconds, accuracy, wpm))
            asyncio.create_task(message.add_reaction(commands.context.TICK))
            if len(messages) != winners:
                return False
            return True

        reference = start.to_reference(fail_if_not_exists=False)
        view = discord.ui.View()
        button = discord.ui.Button(
            style=discord.ButtonStyle.link, label="Jump to Message", url=start.jump_url
        )
        view.add_item(button)
        try:
            await self.bot.wait_for("message", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            if not messages:
                await ctx.send(
                    "No one typed the sentence in time.", reference=reference, view=view
                )
                return
        messages.sort(key=lambda x: x[3], reverse=True)

        descriptions = ["The race ends with the following results:"]
        for n, msgs in enumerate(messages, start=1):
            message, seconds, accuracy, wpm = msgs
            word_length = sum(len(word) for word in quote.split()) / len(quote.split())
            acc = accuracy * 100
            descriptions.append(
                f"{n}. {message.author.mention} [typed the sentence]({message.jump_url}) "
                f"in `{seconds:.2f}s` with **{acc:.2f}%** accuracy. (**{wpm:.1f} WPM**)"
            )
        embed = discord.Embed(color=color, description="\n".join(descriptions))
        await ctx.send(embed=embed, reference=reference, view=view)

    async def get_quote(self) -> Optional[Tuple[str, Optional[str]]]:
        data = {}
        try:
            async with self.session.get("https://zenquotes.io/api/random") as resp:
                quotes = await resp.json()
                data = {"content": quotes[0]["q"], "author": quotes[0]["a"]}
        except aiohttp.ClientConnectionError:
            pass
        if not data:
            try:
                async with self.session.get("https://api.quotable.io/random") as resp:
                    if resp.status == 200:
                        data = await resp.json()
            except aiohttp.ClientConnectionError:
                return None
        return data["content"], data["author"]

    async def render_typerace(self, text: str, color: discord.Color) -> BytesIO:
        func = functools.partial(self.generate_image, text, color)
        task = self.bot.loop.run_in_executor(None, func)
        try:
            return await asyncio.wait_for(task, timeout=60)
        except asyncio.TimeoutError:
            raise commands.UserFeedbackCheckFailure(
                "An error occurred while generating the quote image. Try again later."
            )

    def generate_image(self, text: str, color: discord.Color) -> BytesIO:
        margin = 40
        newline = 30 // 5

        wrapped = textwrap.wrap(text, width=35)
        text = "\n".join(line.strip() for line in wrapped)

        left, right = self.font.getbbox(max(wrapped, key=len))[::2]
        img_width = (right - left) + 2 * margin
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
