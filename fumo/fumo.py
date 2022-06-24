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
from datetime import datetime

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list

from .utils import *


class Fumo(commands.Cog):
    """
    Fumo Fumo. Fumo? Fumo! ᗜˬᗜ
    """

    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.1.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.group()
    async def fumo(self, ctx):
        """Generate a random Fumo ᗜˬᗜ"""
        pass

    @fumo.command()
    async def image(self, ctx):
        """Generates a random Fumo image ᗜˬᗜ"""

        await summon_fumo(ctx, "Image")

    @fumo.command()
    async def gif(self, ctx):
        """Generates a random Fumo GIF ᗜˬᗜ"""

        await summon_fumo(ctx, "GIF")

    @fumo.command()
    async def meme(self, ctx):
        """Generates a random Fumo meme ᗜˬᗜ"""

        await summon_fumo(ctx, "Meme")

    @fumo.command()
    async def video(self, ctx):
        """
        Generates a random Fumo video ᗜˬᗜ

        SPOILER: ||More videos on Fumo Funky Friday ᗜˬᗜ||
        """

        if datetime.today().isoweekday() == 5:
            choice = random.choice(["FUMO FRIDAY", "Video"])
        else:
            choice = "Video"

        await summon_fumo(ctx, choice)

    @commands.command(aliases=["fumopolaroid"])
    async def fumoroid(self, ctx, user: discord.User = None):
        """Generate a Fumo staring at your polaroid avatar."""
        user = user or ctx.author
        async with ctx.typing():
            avatar = await get_avatar(user)
            task = functools.partial(generate_fumoroid, ctx, avatar)
            image = await generate_image(ctx, task)
        if isinstance(image, str):
            await ctx.send(image)
        else:
            await ctx.send(file=image)
