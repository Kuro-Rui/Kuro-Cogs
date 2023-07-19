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
import json
import random
from typing import Literal

import discord
import kuroutils
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path
from redbot.core.utils.chat_formatting import bold

from .utils import *


class Fumo(kuroutils.Cog):
    """Fumo Fumo. Fumo? Fumo! ᗜˬᗜ"""

    __author__ = ["Kuro", "Glas"]
    __version__ = "0.0.2"

    def __init__(self, bot: Red):
        super().__init__(bot)

    @commands.group(invoke_without_command=True)
    async def fumo(self, ctx: commands.Context):
        """Generate a random Fumo ᗜˬᗜ"""

        await self.summon_fumo(ctx)

    @fumo.command()
    async def image(self, ctx: commands.Context):
        """Generates a random Fumo image ᗜˬᗜ"""

        await self.summon_fumo(ctx, "Image")

    @fumo.command()
    async def gif(self, ctx: commands.Context):
        """Generates a random Fumo GIF ᗜˬᗜ"""

        await self.summon_fumo(ctx, "GIF")

    @fumo.command()
    async def video(self, ctx: commands.Context):
        """Generates a random Fumo video ᗜˬᗜ"""

        await self.summon_fumo(ctx, "Video")

    def get_fumos_by_type(self, content_type: Literal["Image", "GIF", "Video"] = None):
        """Get Fumos by type."""
        with open(f"{bundled_data_path(self)}/fumos.json") as f:
            fumos = json.load(f)
        if not content_type:
            return fumos["Image"] + fumos["GIF"] + fumos["Video"]
        return fumos[content_type]

    async def summon_fumo(
        self, ctx: commands.Context, type: Literal["Image", "GIF", "Video"] = None
    ):
        """Summon a Fumo."""
        url = random.choice(self.get_fumos_by_type(type))
        title = f"Here's a Random Fumo! ᗜˬᗜ"
        if type:
            title = f"Here's a Random Fumo {type}! ᗜˬᗜ"
        types = {"jpg": "Image", "png": "Image", "gif": "GIF", "mp4": "Video", "mov": "Video"}
        if await ctx.embed_requested() and types[url[-3:]] != "Video":
            embed = discord.Embed(title=title, color=await ctx.embed_color())
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{bold(title)}\n{url}")

    # Thanks Glas <3
    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["fumopolaroid"])
    async def fumoroid(self, ctx: commands.Context, *, user: discord.User = None):
        """Oh look! A Fumo staring at your polaroid avatar ᗜˬᗜ"""
        user = user or ctx.author
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
    async def marisafie(self, ctx: commands.Context, *, user: discord.User = None):
        """Take a selfie with Marisa. Say cheese! ᗜˬᗜ"""
        user = user or ctx.author
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
    async def marisahat(self, ctx: commands.Context, *, user: discord.User = None):
        """Let's see how do you look after wearing Marisa's hat ᗜˬᗜ"""
        user = user or ctx.author
        async with ctx.typing():
            avatar = await get_avatar(user)
            task = functools.partial(generate_marisahat, ctx, avatar)
            image = await generate_image(ctx, task)
        if isinstance(image, str):
            await ctx.send(image)
        else:
            await ctx.send(file=image)
