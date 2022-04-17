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

import aiohttp
import asyncio
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list

from .utils import summon_fumo


class Fumo(commands.Cog):
    """
    Le Fumo Cog.
    """

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.1.3"

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

    @commands.group()
    async def fumo(self, ctx):
        """Generates Fumo Image."""
        pass

    @fumo.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def random(self, ctx):
        """Generates a random Fumo!"""

        await summon_fumo(self, ctx, "random")

    @fumo.command(aliases=["images"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def image(self, ctx):
        """Generates a random Fumo image."""

        await summon_fumo(self, ctx, "image")

    @fumo.command(aliases=["gifs"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def gif(self, ctx):
        """Generates a random Fumo GIF."""

        await summon_fumo(self, ctx, "gif")

    @fumo.command(aliases=["memes"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meme(self, ctx):
        """Generates a random Fumo meme."""

        await summon_fumo(self, ctx, "meme")
