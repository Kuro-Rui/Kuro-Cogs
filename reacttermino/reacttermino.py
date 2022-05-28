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

import contextlib

import discord
from redbot.core import checks, commands
from redbot.core.utils.chat_formatting import humanize_list
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate

old_restart = None
old_shutdown = None


class ReactTermino(commands.Cog):
    """Shutdown and Restart with confirmation!"""

    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.1.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    def cog_unload(self):
        global old_restart
        if old_restart:
            try:
                self.bot.remove_command("restart")
            except:
                pass
            self.bot.add_command(old_restart)

        global old_shutdown
        if old_shutdown:
            try:
                self.bot.remove_command("shutdown")
            except:
                pass
            self.bot.add_command(old_shutdown)

    @checks.is_owner()
    @commands.command()
    async def restart(self, ctx: commands.Context, directly: bool = False, silently: bool = False):
        """Attempts to restart [botname].

        Makes [botname] quit with exit code 26.

        The restart is not guaranteed: it must be dealt with by the process manager in use.

        You can't restart silently if directly is False.

        **Examples:**
            - `[p]restart`
            - `[p]restart True` - Restart directly without confirmation.
            - `[p]restart True True` - Restart directly without any message.

        **Arguments:**
            - `[directly]` - Whether to directly restart with no confirmation message. Defaults to False.
            - `[silently]` - Whether to skip sending the restart message. Defaults to False & `directly` must be True.
        """
        with contextlib.suppress(discord.HTTPException):
            if directly:
                if silently:
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
    @commands.command()
    async def shutdown(
        self, ctx: commands.Context, directly: bool = False, silently: bool = False
    ):
        """Shuts down the bot.

        Allows [botname] to shut down gracefully.

        This is the recommended method for shutting down the bot.

        **Examples:**
            - `[p]shutdown`
            - `[p]shutdown True` - Shutdown directly without confirmation.
            - `[p]shutdown True True` - Shutdown directly without any message.

        **Arguments:**
            - `[directly]` - Whether to directly shut down with no confirmation message. Defaults to False.
            - `[silently]` - Whether to skip sending the shutdown message. Defaults to False & `directly` must be True.
        """
        with contextlib.suppress(discord.HTTPException):
            if directly:
                if not silently:
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


def setup(bot):
    global old_restart
    old_restart = bot.get_command("restart")
    if old_restart:
        bot.remove_command(old_restart.name)

    global old_shutdown
    old_shutdown = bot.get_command("shutdown")
    if old_shutdown:
        bot.remove_command(old_shutdown.name)

    bot.add_cog(ReactTermino(bot))
