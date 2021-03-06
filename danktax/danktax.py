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

from typing import Union

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list, humanize_number

from .utils import tax, total


class DankTax(commands.Cog):
    """Dank Memer Tax Utility"""

    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.0.2"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.command(aliases=["gettax"])
    async def taxcalc(self, ctx, amount: Union[int, float]):
        """Calculate Dank Memer tax!"""

        amount = round(amount)
        q = humanize_number(amount)
        tq1 = humanize_number(total(amount))
        tq2 = humanize_number(total(amount, False))
        msg = (
            f"*If you send `??? {q}`, you will pay `??? {tq1}`.\n"
            f"To spend `??? {q}` with tax included, send `??? {tq2}`.*"
        )
        examples = (
            f"- `pls trade {amount} @user` = `??? {tq1}`\n"
            f"- `pls trade {total(amount, False)} @user` = `??? {q}`"
        )

        if await ctx.embed_requested():
            tx = humanize_number(tax(amount))
            embed = discord.Embed(title="Tax Calc", description=msg, color=await ctx.embed_color())
            embed.add_field(name="Examples", value=examples)
            embed.set_footer(text=f"Tax: ??? {tx} (Rate: 1%)")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{msg}\n\n**Examples**\n{examples}\n\nTax: ??? {tx} (Rate: 1%)")
