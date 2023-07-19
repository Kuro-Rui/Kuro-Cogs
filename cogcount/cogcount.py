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
import kuroutils
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands.converter import CogConverter


class CogCount(kuroutils.Cog):
    """Count [botname]'s cogs and commands."""

    __author__ = ["Kuro"]
    __version__ = "0.0.1"

    def __init__(self, bot: Red):
        super().__init__(bot)

    @commands.is_owner()
    @commands.group()
    async def count(self, ctx: commands.Context):
        """See how many cogs/commands [botname] has."""
        pass

    @commands.is_owner()
    @count.command()
    async def cogs(self, ctx: commands.Context):
        """See how many cogs [botname] has."""

        total = len(set(await self.bot._cog_mgr.available_modules()))
        loaded = len(set(self.bot.extensions.keys()))
        unloaded = total - loaded

        description = (
            f"`Loaded   :` **{loaded}** Cogs.\n"
            f"`Unloaded :` **{unloaded}** Cogs.\n"
            f"`Total    :` **{total}** Cogs."
        )
        if not await ctx.embed_requested():
            await ctx.send(f"**Cogs**\n\n{description}")
            return
        embed = discord.Embed(
            title="Cogs Count", description=description, color=await ctx.embed_color()
        )
        await ctx.send(embed=embed)

    @commands.is_owner()
    @count.command()
    async def commands(self, ctx: commands.Context, cog: CogConverter = None):
        """
        See how many commands [botname] has.

        You can also provide a cog name to see how many commands is in that cog.
        The commands count includes subcommands.
        """
        if cog:
            commands = len(set(cog.walk_commands()))
            await ctx.send(f"I have `{commands}` commands on that cog.")
            return
        commands = len(set(self.bot.walk_commands()))
        await ctx.send(f"I have `{commands}` commands.")
