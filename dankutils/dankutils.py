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
from random import randint
from typing import Union

import discord
import kuroutils
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import humanize_number

from .utils import *
from .views import DoxxView


class DankUtils(kuroutils.Cog):
    """Dank Memer related commands and utilities!"""

    __author__ = ["Kuro"]
    __version__ = "0.0.2"

    def __init__(self, bot: Red):
        super().__init__(bot)

    @commands.command(aliases=["danktax"])
    async def taxcalc(self, ctx: commands.Context, amount: Union[int, float]):
        """Calculate Dank Memer tax!"""
        amount = round(amount)
        q = humanize_number(amount)
        tq1 = humanize_number(total(amount))
        tq2 = humanize_number(total(amount, False))
        desc = (
            f"*If you send `⏣ {q}`, you will pay `⏣ {tq1}`.\n"
            f"To spend `⏣ {q}` with tax included, send `⏣ {tq2}`.*"
        )
        tx = humanize_number(tax(amount))
        if not await ctx.embed_requested():
            await ctx.send(f"{desc}\n\nTax: ⏣ {tx} (Rate: 1%)")
            return
        embed = discord.Embed(title="Tax Calc", description=desc, color=await ctx.embed_color())
        embed.set_footer(text=f"Tax: ⏣ {tx} (Rate: 1%)")
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 25, commands.BucketType.channel)
    @commands.command(aliases=["heck"])
    async def hack(self, ctx: commands.Context, member: discord.Member):
        """Hack someone!"""
        if member == ctx.author:
            await ctx.send("Umm, please don't DOXX yourself \N{SKULL}")
            return

        # Mass editing lol
        message = await ctx.send(f"{loading(0)} Hacking {member.name} now...")
        await asyncio.sleep(2)
        try:
            await message.edit(content=f"{loading(1)} Finding Discord Login...")
            await asyncio.sleep(2)
            await message.edit(content=f"{loading(2)} Bypassing 2FA...")
            await asyncio.sleep(3)
            email, password = get_email_and_password(member)
            await message.edit(
                content=(
                    f"{loading(3)} Found login information:\n"
                    f"**Email**: `{email}`\n"
                    f"**Password**: `{password}`"
                )
            )
            await asyncio.sleep(4)
            await message.edit(content=f"{loading(0)} Fetching user DMs...")
            await asyncio.sleep(1)
            last_dm = get_last_dm()
            await message.edit(content=f"{loading(1)} **Last DM**: `{last_dm}`")
            await asyncio.sleep(3)
            await message.edit(content=f"{loading(2)} Injecting trojan virus into {member}...")
            await asyncio.sleep(2)
            await message.edit(content=f"{loading(3)} Virus injected. Finding IP Address...")
            await asyncio.sleep(3)
            # A valid IP address must be in the form of x.x.x.x, where x is a number from 0-255.
            ip_address = f"{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}"
            await message.edit(content=f"{loading(0)} **IP Address**: `{ip_address}`")
            await asyncio.sleep(2)
            await message.edit(content=f"{loading(1)} Selling user data to the government...")
            await asyncio.sleep(2)
            await message.edit(
                content=f"{loading(2)} Reporting account to Discord for breaking ToS..."
            )
            await asyncio.sleep(1)
            await message.edit(content=f"{commands.context.TICK} Finished hacking {member.name}.")
            info = format_doxx_info(email, password, ip_address, last_dm)
            info_embed = discord.Embed(
                title="Hack Information", description=info, color=await ctx.embed_color()
            )
            view = DoxxView(info_embed=info_embed)
            await view.start(ctx, "The *totally* real and dangerous hack is complete.")
        except discord.NotFound:
            await ctx.send("Process terminated. The hack failed.")
            return
