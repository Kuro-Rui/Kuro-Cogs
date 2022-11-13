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

import asyncio
import functools
import random
from typing import Literal

import aiohttp
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, humanize_list

from .utils import *


class Fumo(commands.Cog):
    """
    Fumo Fumo. Fumo? Fumo! ᗜˬᗜ
    """

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    __author__ = humanize_list(["Kuro", "Glas"])
    __version__ = "1.2.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    def cog_unload(self):
        asyncio.create_task(self.session.close())

    @commands.group(invoke_without_command=True)
    async def fumo(self, ctx):
        """Generate a random Fumo ᗜˬᗜ"""

        await self.summon_fumo(ctx)

    @fumo.command()
    async def image(self, ctx):
        """Generates a random Fumo image ᗜˬᗜ"""

        await self.summon_fumo(ctx, "Image")

    @fumo.command()
    async def gif(self, ctx):
        """Generates a random Fumo GIF ᗜˬᗜ"""

        await self.summon_fumo(ctx, "GIF")

    @fumo.command()
    async def video(self, ctx):
        """Generates a random Fumo video ᗜˬᗜ"""

        await self.summon_fumo(ctx, "Video")

    @staticmethod
    def get_fumo_type(url: str) -> Literal["Image", "GIF", "Video"]:
        """Get the type of a Fumo."""
        types = {"jpg": "Image", "png": "Image", "gif": "GIF", "mp4": "Video"}
        type = types[url[-3:]]
        return type

    async def get_fumos_by_type(self, content_type: Literal["Image", "GIF", "Video"] = None):
        """Get Fumos by type."""
        urls = []
        async with self.session.get("https://fumo-api.nosesisaid.com/") as response:
            if response.status == 200:
                data = await response.json()
                for dict in data:
                    url = dict["URL"]
                    type = self.get_fumo_type(url)
                    if type == content_type:
                        urls.append(url)
        return urls

    async def summon_fumo(
        self, ctx: commands.Context, type: Literal["Image", "GIF", "Video"] = None
    ):
        """Summon a Fumo."""
        error_msg = "Oh no! Gensokyo is on attack, so no Fumos. Try again later ᗜˬᗜ (API Issue)"
        if not type:
            async with self.session.get("https://fumo-api.nosesisaid.com/random") as response:
                if response.status == 200:
                    data = await response.json()
                    url = data["URL"]
                    type = self.get_fumo_type(url)
                else:
                    return await ctx.send(error_msg)
        else:
            urls = await self.get_fumos_by_type(type)
            if not urls:
                return await ctx.send(error_msg)
            url = random.choice(urls)

        title = f"Here's a Random Fumo {type}! ᗜˬᗜ"
        if await ctx.embed_requested() and type != "Video":
            embed = discord.Embed(title=title, color=await ctx.embed_color())
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{bold(title)}\n{url}")

    # Thanks Glas!
    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["fumopolaroid"])
    async def fumoroid(self, ctx, *, user: discord.User = None):
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

    # Thanks Glas!
    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["marisaselfie"])
    async def marisafie(self, ctx, *, user: discord.User = None):
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
