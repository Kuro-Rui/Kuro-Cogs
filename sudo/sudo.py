# Credits to jack1142 for the idea. (https://github.com/Cog-Creators/Red-DiscordBot/pull/5419)

import asyncio
from copy import copy
from datetime import timedelta

import discord
from redbot.core import commands
from redbot.core.commands import TimedeltaConverter
from redbot.core.utils.chat_formatting import humanize_list, humanize_timedelta

from .utils import is_owner


class Sudo(commands.Cog):
    """Allows dropping and elevating owner permissions!"""

    def __init__(self, bot):
        self.bot = bot
        self.all_owner_ids = copy(self.bot.owner_ids)
        self.bot.owner_ids.clear()

    def cog_unload(self):
        self.bot.owner_ids.update(copy(self.all_owner_ids))
        self.all_owner_ids.clear()

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

    @is_owner(real=False, copied=True)
    @commands.command()
    async def su(self, ctx: commands.Context):
        """Enable your bot owner privileges."""
        self.bot.owner_ids.add(ctx.author.id)
        await ctx.send("Your bot owner privileges have been enabled.")

    @is_owner(real=True, copied=False)
    @commands.command()
    async def unsu(self, ctx: commands.Context):
        """Disable your bot owner privileges."""
        self.bot.owner_ids.remove(ctx.author.id)
        await ctx.send("Your bot owner privileges have been disabled.")

    @is_owner(real=False, copied=True)
    @commands.command()
    async def sudo(self, ctx: commands.Context, *, command: str):
        """Runs the specified command with bot owner permissions.

        The prefix must not be entered.
        """
        self.bot.owner_ids.add(ctx.author.id)
        msg = ctx.message
        msg.content = ctx.prefix + command
        context = await ctx.bot.get_context(msg)
        await ctx.bot.invoke(context)
        if self.bot.get_cog("Sudo"):  # Worst condition if the command is "unload sudo".
            self.bot.owner_ids.remove(ctx.author.id)

    @is_owner(real=False, copied=True)
    @commands.command()
    async def sutimeout(
        self,
        ctx: commands.Context,
        *,
        interval: TimedeltaConverter(
            minimum=timedelta(minutes=1),
            maximum=timedelta(days=1),
            default_unit="minutes",
        ) = timedelta(minutes=15),
    ):
        """Enable your bot owner privileges for the specified time.

        Should be between 1 minute and 1 day. Default is 15 minutes.
        """
        time = interval.total_seconds()
        self.bot.owner_ids.add(ctx.author.id)
        await ctx.send(
            f"Your bot owner privileges have been enabled for {humanize_timedelta(seconds=time)}."
        )
        await asyncio.sleep(time)
        if self.bot.get_cog("Sudo"):
            self.bot.owner_ids.remove(ctx.author.id)
