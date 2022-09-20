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

import calendar
import random
from datetime import datetime

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, humanize_list

from .converters import Month, Year

NOW = datetime.utcnow()


class Calendar(commands.Cog):
    """See the calendar on Discord!"""

    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.0.1"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.command(name="calendar")
    async def _calendar(self, ctx, month: Month = NOW.month, year: Year = NOW.year):
        """View the calendar!"""
        ordinal = lambda n: "%d%s" % (
            n,
            "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4],
        )
        d_m_y = f"{ordinal(NOW.day)} {NOW.strftime('%B')} {year}"
        cal = calendar.month(year, month, w=4 if ctx.author.is_on_mobile() else 5, l=2)
        if await ctx.embed_requested():
            embed = discord.Embed(
                description=box(cal, lang="prolog"), color=await ctx.embed_color()
            )
            embed.set_image(url=f"https://picsum.photos/id/{random.randint(1, 1084)}/500/200")
            embed.set_footer(text=f"Date: {d_m_y}")
            return await ctx.send(embed=embed)
        await ctx.send(box(cal, lang="prolog"))
