"""
MIT License

Copyright (c) 2021-present Kuro-Rui

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

import functools
import random
from typing import Literal, Optional

import aiohttp
import discord
import kuroutils
from discord.ext import tasks
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import bold

from .object import Fumos
from .utils import *


class Fumo(kuroutils.Cog):
    """Fumo Fumo. Fumo? Fumo! ᗜˬᗜ"""

    __author__ = ["Kuro", "Glas"]
    __version__ = "0.1.2"

    def __init__(self, bot: Red):
        super().__init__(bot)
        self.fumos: Optional[Fumos] = None
        self.session = aiohttp.ClientSession()

    async def cog_load(self):
        await super().cog_load()
        self.fetch_fumos_loop.start()

    async def cog_unload(self):
        super().cog_unload()
        self.fetch_fumos_loop.stop()
        await self.session.close()

    # 10 loops a day is enough imo :p
    @tasks.loop(hours=2.4)
    async def fetch_fumos_loop(self):
        await self.fetch_fumos()

    async def fetch_fumos(self):
        async with self.session.get("https://kuro-rui.github.io/API/fumo/all.json") as resp:
            if resp.status != 200:
                self._log.debug("Failed to fetch Fumos.")
                return
            self.fumos = Fumos(**await resp.json())
            self._log.debug("Successfully fetched Fumos.")

    @commands.group(invoke_without_command=True)
    async def fumo(self, ctx: commands.Context):
        """Generate a random Fumo ᗜˬᗜ"""

        await self.summon_fumo(ctx)

    @commands.check(lambda ctx: discord.utils.utcnow().weekday() == 4)
    @fumo.command()
    async def friday(self, ctx: commands.Context):
        """Generates a random Fumo Friday video ᗜˬᗜ"""

        await self.summon_fumo(ctx, "friday")

    @fumo.command()
    async def gif(self, ctx: commands.Context):
        """Generates a random Fumo GIF ᗜˬᗜ"""

        await self.summon_fumo(ctx, "gif")

    @fumo.command()
    async def image(self, ctx: commands.Context):
        """Generates a random Fumo image ᗜˬᗜ"""

        await self.summon_fumo(ctx, "image")

    @fumo.command()
    async def video(self, ctx: commands.Context):
        """Generates a random Fumo video ᗜˬᗜ"""

        await self.summon_fumo(ctx, "video")

    async def summon_fumo(
        self,
        ctx: commands.Context,
        fumo_type: Literal["all", "friday", "gif", "image", "video"] = "all",
    ) -> None:
        """Summon a Fumo."""
        if not self.fumos:
            message = "Fumos are not available at the moment. Please try again later."
            if await self.bot.is_owner(ctx.author):
                message += "\nPlease contact the cog author if this issue persists."
            await ctx.send(message)
            return
        url = random.choice(getattr(self.fumos, fumo_type))
        title = "Here's a Random Fumo! ᗜˬᗜ"
        if fumo_type != "all":
            fumo_type = "GIF" if fumo_type == "gif" else fumo_type.capitalize()
            title = f"Here's a Random Fumo {fumo_type}! ᗜˬᗜ"
        if await ctx.embed_requested() and url[-3:] not in ("mp4", "mov"):
            embed = discord.Embed(title=title, color=await ctx.embed_color())
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{bold(title)}\n{url}")

    # Thanks Glas <3
    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["fumopolaroid"])
    async def fumoroid(self, ctx: commands.Context, *, user: discord.User = commands.Author):
        """Oh look! A Fumo staring at your polaroid avatar ᗜˬᗜ"""
        async with ctx.typing():
            avatar = await get_avatar(user)
            task = functools.partial(generate_fumoroid, ctx, avatar)
            image = await generate_image(ctx, task)
        if isinstance(image, str):
            await ctx.send(image)
        else:
            await ctx.send(file=image)

    # Thanks Glas <3
    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["marisaselfie"])
    async def marisafie(self, ctx: commands.Context, *, user: discord.User = commands.Author):
        """Take a selfie with Marisa. Say cheese! ᗜˬᗜ"""
        async with ctx.typing():
            avatar = await get_avatar(user)
            task = functools.partial(generate_marisafie, ctx, avatar)
            image = await generate_image(ctx, task)
        if isinstance(image, str):
            await ctx.send(image)
        else:
            await ctx.send(file=image)

    # Thanks Glas <3
    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    async def marisahat(self, ctx: commands.Context, *, user: discord.User = commands.Author):
        """Let's see how do you look after wearing Marisa's hat ᗜˬᗜ"""
        async with ctx.typing():
            avatar = await get_avatar(user)
            task = functools.partial(generate_marisahat, ctx, avatar)
            image = await generate_image(ctx, task)
        if isinstance(image, str):
            await ctx.send(image)
        else:
            await ctx.send(file=image)
