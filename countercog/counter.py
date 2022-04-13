import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list


class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.0.1"

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

        total = len(set(await ctx.bot._cog_mgr.available_modules()))
        loaded = len(set(ctx.bot.extensions.keys()))
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
            if self.bot.get_cog(cog):
                cmds = sum(1 for _ in self.bot.get_cog(cog).walk_commands())
                await ctx.send(f"I have `{cmds}` commands on that cog.")
            else:
                await ctx.send("Please provide a valid cog name. (Example: `CounterCog`)")
        else:
            cmds = len(self.bot.commands)
            await ctx.send(f"I have `{cmds}` commands.")
