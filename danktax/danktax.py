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

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list, humanize_number

from .utils import percent, tax, total


class DankTax(commands.Cog):
    """Dank Memer Tax Utility"""

    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.command(aliases=["gettax"])
    async def taxcalc(self, ctx, quantity: int):
        """Calculate your Dank Memer tax!"""

        q = humanize_number(quantity)
        msg = (
            f"*If you send `⏣ {q}`, you will pay `⏣ {total(quantity)}`.\n"
            f"To spend `⏣ {q}` with tax included, send `⏣ {total(quantity, False)}`.*"
        )
        examples = (
            f"- `pls trade {q} @user` = `⏣ {total(quantity)}`\n"
            f"- `pls trade {total(quantity, False)} @user` = `⏣ {q}`"
        )

        if await ctx.embed_requested():
            embed = discord.Embed(title="Tax Calc", description=msg, color=await ctx.embed_color())
            embed.add_field(name="Examples", value=examples)
            embed.set_footer(f"Tax: ⏣ {tax(quantity)} (Rate: 1%)")
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"{msg}\n\n**Examples**\n{examples}\n\nTax: ⏣ {tax(quantity)} (Rate: 1%)"
            )
