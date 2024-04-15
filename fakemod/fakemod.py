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
from typing import Literal, Optional

import discord
import kuroutils
from kuroutils.converters import Emoji
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils.predicates import MessagePredicate

from .converters import Action


# Inspired by Jeff (https://github.com/Noa-DiscordBot/Noa-Cogs/blob/main/fakemod/fakemod.py)
class FakeMod(kuroutils.Cog):
    """Fake moderation tools to prank your friends!"""

    __author__ = ["Kuro"]
    __version__ = "0.1.1"

    def __init__(self, bot: Red):
        super().__init__(bot)
        self._config = Config.get_conf(self, 9863948134, True)
        self._config.register_guild(
            channel=None,
            case_id=1,
            warn_emoji="\N{HEAVY HEART EXCLAMATION MARK ORNAMENT}\N{VARIATION SELECTOR-16}",
            mute_emoji="\N{FACE WITH FINGER COVERING CLOSED LIPS}",
            kick_emoji="\N{HIGH-HEELED SHOE}",
            ban_emoji="\N{COLLISION SYMBOL}",
        )

    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    @commands.group()
    async def fakemodlogset(self, ctx: commands.Context):
        """Manage fake modlog settings."""
        pass

    @fakemodlogset.command(aliases=["channel"])
    async def modlog(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """
        Set a channel as the fake modlog.

        Omit [channel] to disable the fake modlog.
        """
        if channel:
            if ctx.channel.permissions_for(channel.guild.me).send_messages:
                await self._config.guild(ctx.guild).channel.set(channel.id)
                await ctx.send(f"Fake mod events will be sent to {channel.mention}.")
            else:
                await ctx.send("Please grant me permission to send message in that channel first.")
        else:
            await self._config.guild(ctx.guild).channel.clear()
            await ctx.send("Fake mod log deactivated.")

    @fakemodlogset.command()
    async def emoji(self, ctx: commands.Context, action: Action = None, emoji: Emoji = None):
        """
        Set an emoji for a fake mod action.

        The `action` should be either `warn`, `mute`, `kick`, or `ban`.
        """

        config = await self._config.guild(ctx.guild).all()
        if not action:
            await ctx.send(
                (
                    f"**__Current Settings__:**\n"
                    f"`Fake Warn :` {config['warn_emoji']}\n"
                    f"`Fake Mute :` {config['mute_emoji']}\n"
                    f"`Fake Kick :` {config['kick_emoji']}\n"
                    f"`Fake Ban  :` {config['ban_emoji']}"
                )
            )
            return
        async with self._config.guild(ctx.guild).all() as guild_settings:
            guild_settings[f"{action}_emoji"] = str(emoji) if emoji else None
        if not emoji:
            await ctx.send(f"The emoji for `fake {action}` has been reset.")
            return
        await ctx.send(f"Emoji for `fake {action}` has been set to {emoji}.")

    @fakemodlogset.command()
    async def resetcases(self, ctx: commands.Context):
        """Reset all fake modlog cases in this server."""
        await ctx.send("Would you like to reset all fake modlog cases in this server? (yes/no)")
        try:
            check = MessagePredicate.yes_or_no(ctx, user=ctx.author)
            await ctx.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        if check.result:
            await self._config.guild(ctx.guild).case_id.set(1)
            await ctx.send("Cases have been reset.")
        else:
            await ctx.send("No changes have been made.")

    async def send_fake_modlog(
        self,
        guild: discord.Guild,
        action: Literal["warn", "unwarn", "mute", "unmute", "kick", "ban", "unban"],
        member: discord.Member,
        moderator: discord.Member,
        reason: Optional[str],
    ):
        config = await self._config.guild(guild).all()
        if config["channel"] and (fake_modlog := self.bot.get_channel(config["channel"])):
            case_id: int = config["case_id"]
            await self._config.guild(guild).case_id.set(case_id + 1)
            action = action.replace("un", "")
            emoji = config[f"{action}_emoji"]
            reason = reason or "Not provided."
            embed = discord.Embed(
                title=f"Case #{case_id} | {action.capitalize()} {emoji}",
                description=f"**Reason:** {reason}",
                timestamp=discord.utils.utcnow(),
            )
            embed.set_author(name=f"{member} ({member.id})")
            embed.add_field(name="Moderator", value=f"{moderator} ({moderator.id})")
            embed.set_footer(text="just kidding lol")
            await fake_modlog.send(embed=embed)

    @commands.guild_only()
    @commands.command(name="worn")
    async def fake_warn(
        self, ctx: commands.Context, member: discord.Member, *, reason: str = None
    ):
        """Fake warn a member for the specified reason."""
        if member == ctx.me:
            await ctx.send("You can't warn me.")
            return
        if member == ctx.author:
            await ctx.send("You can't warn yourself.")
            return
        await ctx.send(f"**{member}** has been warned.")
        await self.send_fake_modlog(ctx.guild, "warn", member, ctx.author, reason)

    @commands.guild_only()
    @commands.command(name="unworn")
    async def fake_unwarn(
        self, ctx: commands.Context, member: discord.Member, *, reason: str = None
    ):
        """Fake unwarn a member for the specified reason."""
        if member == ctx.author:
            await ctx.send("You can't unwarn yourself.")
            return
        await ctx.send(f"**{member}** has been unwarned.")
        await self.send_fake_modlog(ctx.guild, "unwarn", member, ctx.author, reason)

    @commands.guild_only()
    @commands.command(name="myut", aliases=["moot"])
    async def fake_mute(
        self, ctx: commands.Context, member: discord.Member, *, reason: str = None
    ):
        """Fake mute a member."""
        if member == ctx.me:
            await ctx.send("You can't mute me.")
            return
        if member == ctx.author:
            await ctx.send("You can't mute yourself.")
            return
        await ctx.send(f"**{member}** has been muted in this server.")
        await self.send_fake_modlog(ctx.guild, "mute", member, ctx.author, reason)

    @commands.guild_only()
    @commands.command(name="unmyut", aliases=["unmoot"])
    async def fake_unmute(
        self, ctx: commands.Context, member: discord.Member, *, reason: str = None
    ):
        """Fake unmute a member."""
        if member == ctx.author:
            await ctx.send("You can't unmute yourself.")
            return
        await ctx.send(f"**{member}** has been unmuted in this server.")
        await self.send_fake_modlog(ctx.guild, "unmute", member, ctx.author, reason)

    @commands.guild_only()
    @commands.command(name="kik", aliases=["kek", "keck"])
    async def fake_kick(
        self, ctx: commands.Context, member: discord.Member, *, reason: str = None
    ):
        """Fake kick a member."""
        if member == ctx.me:
            await ctx.send("You can't kick me.")
            return
        if member == ctx.author:
            await ctx.send("You can't kick yourself.")
            return
        await ctx.send(f"**{member}** has been kicked from the server.")
        await self.send_fake_modlog(ctx.guild, "kick", member, ctx.author, reason)

    @commands.guild_only()
    @commands.command(name="ben", aliases=["bam", "bon", "beam", "bean"])
    async def fake_ban(self, ctx: commands.Context, user: discord.User, *, reason: str = None):
        """Fake ban a user."""
        if user == ctx.me:
            await ctx.send("You can't ban me.")
            return
        if user == ctx.author:
            await ctx.send("You can't ban yourself.")
            return
        await ctx.send(f"**{user}** has been banned from the server.")
        await self.send_fake_modlog(ctx.guild, "ban", user, ctx.author, reason)

    @commands.guild_only()
    @commands.command(name="unben", aliases=["unbam", "unbon", "unbeam", "unbean"])
    async def fake_unban(self, ctx: commands.Context, user: discord.User, *, reason: str = None):
        """Fake unban a user."""
        if user == ctx.author:
            await ctx.send("You can't unban yourself.")
            return
        await ctx.send(f"**{user}** has been unbanned from the server.")
        await self.send_fake_modlog(ctx.guild, "unban", user, ctx.author, reason)
