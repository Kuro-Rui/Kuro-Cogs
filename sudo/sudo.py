"""
Red - A fully customizable Discord bot
Copyright (C) 2017-present Cog Creators
Copyright (C) 2015-2017 Twentysix

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Credits to Draper & Jack for the idea. (https://github.com/Cog-Creators/Red-DiscordBot/pull/5419)

import asyncio
import datetime
from copy import copy

import kuroutils
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands import TimedeltaConverter
from redbot.core.utils.chat_formatting import humanize_timedelta

from .utils import is_owner


class Sudo(kuroutils.Cog):
    """Allows dropping and elevating owner permissions!"""

    __author__ = ["Draper", "jack1142 (Jackenmen#6607)", "Kuro"]
    __version__ = "0.0.1"

    def __init__(self, bot: Red):
        super().__init__(bot)
        self.all_owner_ids = copy(self.bot.owner_ids)
        self.bot.owner_ids.clear()

    async def cog_unload(self):
        super().cog_unload()
        self.bot.owner_ids.update(copy(self.all_owner_ids))
        self.all_owner_ids.clear()

    @is_owner(copied=True)
    @commands.command()
    async def su(self, ctx: commands.Context):
        """Enable your bot owner privileges."""
        self.bot.owner_ids.add(ctx.author.id)
        self.all_owner_ids.remove(ctx.author.id)
        await ctx.send("Your bot owner privileges have been enabled.")

    @is_owner(real=True)
    @commands.command()
    async def unsu(self, ctx: commands.Context):
        """Disable your bot owner privileges."""
        self.all_owner_ids.add(ctx.author.id)
        self.bot.owner_ids.remove(ctx.author.id)
        await ctx.send("Your bot owner privileges have been disabled.")

    @is_owner(copied=True)
    @commands.command()
    async def sutimeout(
        self,
        ctx: commands.Context,
        *,
        interval: TimedeltaConverter(
            minimum=datetime.timedelta(minutes=1),
            maximum=datetime.timedelta(days=1),
            default_unit="minutes",  # noqa: F821
        ) = datetime.timedelta(minutes=15),
    ):
        """
        Enable your bot owner privileges for the specified time.

        Should be between 1 minute and 1 day. Default is 15 minutes.
        """
        self.bot.owner_ids.add(ctx.author.id)
        self.all_owner_ids.remove(ctx.author.id)
        time = interval.total_seconds()
        await ctx.send(
            f"Your bot owner privileges have been enabled for {humanize_timedelta(seconds=time)}."
        )
        await asyncio.sleep(time)
        if self.bot.get_cog("Sudo"):  # Worst condition if user unloaded sudo.
            self.all_owner_ids.add(ctx.author.id)
            self.bot.owner_ids.remove(ctx.author.id)

    @is_owner(copied=True)
    @commands.command()
    async def sudo(self, ctx: commands.Context, *, command: str):
        """
        Runs the specified command with bot owner permissions.

        The prefix must not be entered.
        """
        self.bot.owner_ids.add(ctx.author.id)
        self.all_owner_ids.remove(ctx.author.id)
        message = copy(ctx.message)
        message.content = ctx.prefix + command
        context = await self.bot.get_context(message)
        await self.bot.invoke(context)  # Doesn't work for tags tho
        if self.bot.get_cog("Sudo"):  # Worst condition if the command is "unload sudo".
            self.all_owner_ids.add(ctx.author.id)
            self.bot.owner_ids.remove(ctx.author.id)

    @is_owner(copied=True)
    @commands.command()
    async def sudomsg(self, ctx: commands.Context, *, content: str = ""):
        """
        Dispatch a message event as if it were sent by bot owner.

        Current message is used as a base (including attachments, embeds, etc.)

        Note: If `content` isn't passed, the message needs to contain embeds, attachments,
        or anything else that makes the message non-empty.
        """
        message = ctx.message
        if not content and not message.embeds and not message.attachments:
            # DEP-WARN: add `message.stickers` when adding d.py 2.0
            await ctx.send_help()
            return
        self.bot.owner_ids.add(ctx.author.id)
        self.all_owner_ids.remove(ctx.author.id)
        msg = copy(message)
        msg.content = content
        self.bot.dispatch("message", msg)
        if self.bot.get_cog("Sudo"):  # Worst condition if the content is "[p]unload sudo".
            self.all_owner_ids.add(ctx.author.id)
            self.bot.owner_ids.remove(ctx.author.id)
