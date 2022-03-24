import contextlib

import discord
from redbot.core import checks, commands
from redbot.core.utils.chat_formatting import humanize_list
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions


class ReactTermino(commands.Cog):
    """Shutdown and Restart with confirmation!"""

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

    @checks.is_owner()
    @commands.command(name="restart", usage="[directly=False]")
    async def _restart(self, ctx: commands.Context, directly: bool = False):
        """Attempts to restart [botname].

        Makes [botname] quit with exit code 26.
        The restart is not guaranteed: it must be dealt with by the process manager in use.

        **Examples:**
            - `[p]restart`
            - `[p]restart True` - Restart directly without confirmation.

        **Arguments:**
            - `[directly]` - Whether to directly restart with no confirmation message. Defaults to False.
        """
        with contextlib.suppress(discord.HTTPException):
            if directly:
                emb = discord.Embed(title="Restarting...", color=await ctx.embed_color())
                await ctx.send(embed=emb)
                await self.bot.shutdown(restart=True)
            else:
                emb = discord.Embed(
                    title="Are you sure you want to restart?", color=await ctx.embed_color()
                )
                msg = await ctx.send(embed=emb)
                start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
                pred = ReactionPredicate.yes_or_no(msg, ctx.author)
                await ctx.bot.wait_for("reaction_add", check=pred)
                if pred.result is True:
                    emb = discord.Embed(title="Restarting...", color=await ctx.embed_color())
                    await msg.edit(embed=emb)
                    await self.bot.shutdown(restart=True)
                else:
                    emb = discord.Embed(title="Cancelling...", color=await ctx.embed_color())
                    await msg.edit(embed=emb)

    @checks.is_owner()
    @commands.command(name="shutdown", usage="[directly=False]")
    async def _shutdown(self, ctx: commands.Context, directly: bool = False):
        """Shuts down the bot.

        Allows [botname] to shut down gracefully.

        This is the recommended method for shutting down the bot.

        **Examples:**
            - `[p]shutdown`
            - `[p]shutdown True` - Shutdown directly without confirmation.

        **Arguments:**
            - `[directly]` - Whether to directly shut down with no confirmation message. Defaults to False.
        """
        with contextlib.suppress(discord.HTTPException):
            if directly:
                emb = discord.Embed(title="Shutting Down...", color=await ctx.embed_color())
                await ctx.send(embed=emb)
                await self.bot.shutdown()
            else:
                emb = discord.Embed(
                    title="Are you sure you want to shut down?", color=await ctx.embed_color()
                )
                msg = await ctx.send(embed=emb)
                start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
                pred = ReactionPredicate.yes_or_no(msg, ctx.author)
                await ctx.bot.wait_for("reaction_add", check=pred)
                if pred.result is True:
                    emb = discord.Embed(title="Shutting Down...", color=await ctx.embed_color())
                    await msg.edit(embed=emb)
                    await self.bot.shutdown()
                else:
                    emb = discord.Embed(title="Cancelling...", color=await ctx.embed_color())
                    await msg.edit(embed=emb)
