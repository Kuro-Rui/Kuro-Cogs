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
from redbot.core.utils.chat_formatting import humanize_list


class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.0.3"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.is_owner()
    @commands.group()
    async def count(self, ctx):
        """Count your cogs/commands."""
        pass

    @commands.is_owner()
    @count.command()
    async def cogs(self, ctx):
        """Count your cogs."""

        total = len(set(await self.bot._cog_mgr.available_modules()))
        loaded = len(set(self.bot.extensions.keys()))
        unloaded = total - loaded

        msg = (
            f"`Loaded   :` **{loaded}** Cogs.\n"
            f"`Unloaded :` **{unloaded}** Cogs.\n"
            f"`Total    :` **{total}** Cogs."
        )
        if await ctx.embed_requested():
            embed = discord.Embed(title="Cogs", description=msg, color=await ctx.embed_color())
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"**Cogs**\n\n{msg}")

    @commands.is_owner()
    @count.command()
    async def commands(self, ctx, cog: str = None):
        """
        Count your commands.

        You can also provide a cog name to see how many commands is in that cog.
        The commands count includes subcommands.
        """
        if cog:
            if not self.bot.get_cog(cog):
                return await ctx.send("I can't find that cog.")
            cog = self.bot.get_cog(cog)
            cmds = len(set(cog.walk_commands()))
            await ctx.send(f"I have `{cmds}` commands on that cog.")
        else:
            cmds = len(set(self.bot.walk_commands()))
            await ctx.send(f"I have `{cmds}` commands.")
