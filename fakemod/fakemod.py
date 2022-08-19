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

import datetime
from asyncio import TimeoutError

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import humanize_list
from redbot.core.utils.predicates import MessagePredicate

from .converters import Action, Emoji


# Inspired by Jeff (https://github.com/Noa-DiscordBot/Noa-Cogs/blob/main/fakemod/fakemod.py)
class FakeMod(commands.Cog):
    """Fake Moderation Tools."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 9863948134, True)
        self.config.register_guild(
            channel=None,
            case_id=1,
            warn_emoji="\N{HEAVY HEART EXCLAMATION MARK ORNAMENT}\N{VARIATION SELECTOR-16}",
            mute_emoji="\N{FACE WITH FINGER COVERING CLOSED LIPS}",
            kick_emoji="\N{HIGH-HEELED SHOE}",
            ban_emoji="\N{COLLISION SYMBOL}",
        )

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.1.1"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    @commands.group()
    async def fakemodlogset(self, ctx):
        """Manage fake modlog settings."""
        pass

    @fakemodlogset.command(aliases=["channel"])
    async def modlog(self, ctx, channel: discord.TextChannel = None):
        """
        Set a channel as the fake modlog.
        Omit [channel] to disable the fake modlog.
        """
        if channel:
            if ctx.channel.permissions_for(channel.guild.me).send_messages:
                await self.config.guild(ctx.guild).channel.set(channel.id)
                await ctx.send(f"Fake mod events will be sent to {channel.mention}.")
            else:
                await ctx.send("Please grant me permission to send message in that channel first.")
        else:
            await self.config.guild(ctx.guild).channel.clear()
            await ctx.send("Fake mod log deactivated.")

    @fakemodlogset.command()
    async def emoji(self, ctx, action: Action = None, emoji: Emoji = None):
        """
        Set an emoji for a fake mod action.

        `action` should be either `warn`, `mute`, `kick`, or `ban`.
        """

        warn_emoji = await self.config.guild(ctx.guild).warn_emoji()
        mute_emoji = await self.config.guild(ctx.guild).mute_emoji()
        kick_emoji = await self.config.guild(ctx.guild).kick_emoji()
        ban_emoji = await self.config.guild(ctx.guild).ban_emoji()

        if not action:
            await ctx.send_help()
            return await ctx.send(
                (
                    "**__Current Settings__:**\n"
                    "`Fake Warn :` {}\n"
                    "`Fake Mute :` {}\n"
                    "`Fake Kick :` {}\n"
                    "`Fake Ban  :` {}\n"
                ).format(warn_emoji, mute_emoji, kick_emoji, ban_emoji)
            )
        if action == "warn":
            if not emoji:
                await self.config.guild(ctx.guild).warn_emoji.clear()
                return await ctx.send("The emoji has been reset.")
            await self.config.guild(ctx.guild).warn_emoji.set(emoji)
            await ctx.send("Emoji for fake `warn` has been set.")
        elif action == "mute":
            if not emoji:
                await self.config.guild(ctx.guild).mute_emoji.clear()
                return await ctx.send("The emoji has been reset.")
            await self.config.guild(ctx.guild).mute_emoji.set(emoji)
            await ctx.send("Emoji for fake `mute` has been set.")
        elif action == "kick":
            if not emoji:
                await self.config.guild(ctx.guild).kick_emoji.clear()
                return await ctx.send("The emoji has been reset.")
            await self.config.guild(ctx.guild).kick_emoji.set(emoji)
            await ctx.send("Emoji for fake `kick` has been set.")
        elif action == "ban":
            if not emoji:
                await self.config.guild(ctx.guild).ben_emoji.clear()
                return await ctx.send("The emoji has been reset.")
            await self.config.guild(ctx.guild).ban_emoji.set(emoji)
            await ctx.send("Emoji for fake `ban` has been set.")

    @fakemodlogset.command()
    async def resetcases(self, ctx):
        """Reset all fake modlog cases in this server."""
        await ctx.send("Would you like to reset all fake modlog cases in this server? (yes/no)")
        try:
            pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
            await ctx.bot.wait_for("message", check=pred, timeout=30)
        except TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        if pred.result:
            await self.config.guild(ctx.guild).case_id.set(1)
            await ctx.send("Cases have been reset.")
        else:
            await ctx.send("No changes have been made.")

    @commands.command(name="worn")
    async def fake_warn(self, ctx, member: discord.Member, reason: str = None):
        """Fake warn a member for the specified reason."""
        if member == ctx.me:
            await ctx.send("You can't warn me.")
        elif member == ctx.author:
            await ctx.send("You can't warn yourself.")
        else:
            await ctx.tick()
            channel = await self.config.guild(ctx.guild).channel()
            if channel and self.bot.get_channel(channel):
                fake_modlog = self.bot.get_channel(channel)
                case_id: int = await self.config.guild(ctx.guild).case_id()
                await self.config.guild(ctx.guild).case_id.set(case_id + 1)
                emoji = await self.config.guild(ctx.guild).warn_emoji()
                reason = reason if reason else "Not provided."
                embed = discord.Embed(
                    title=f"Case #{case_id} | Warn {emoji}", description=f"**Reason:** {reason}"
                )
                embed.set_author(name=f"{member} ({member.id})")
                embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})")
                embed.set_footer(text="just kidding lol")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                await fake_modlog.send(embed=embed)

    @commands.command(name="myut", aliases=["moot"])
    async def fake_mute(self, ctx, member: discord.Member, *, reason: str = None):
        """Fake mute a member."""
        if member == ctx.me:
            await ctx.send("You can't mute me.")
        elif member == ctx.author:
            await ctx.send("You can't mute yourself.")
        else:
            await ctx.send(f"{member} has been muted in this server.")
            channel = await self.config.guild(ctx.guild).channel()
            if channel and self.bot.get_channel(channel):
                fake_modlog = self.bot.get_channel(channel)
                case_id: int = await self.config.guild(ctx.guild).case_id()
                await self.config.guild(ctx.guild).case_id.set(case_id + 1)
                emoji = await self.config.guild(ctx.guild).mute_emoji()
                reason = reason if reason else "Not provided."
                embed = discord.Embed(
                    title=f"Case #{case_id} | Mute {emoji}", description=f"**Reason:** {reason}"
                )
                embed.set_author(name=f"{member} ({member.id})")
                embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})")
                embed.set_footer(text="just kidding lol")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                await fake_modlog.send(embed=embed)

    @commands.command(name="kik", aliases=["kek", "keck"])
    async def fake_kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Fake kick a member."""
        if member == ctx.me:
            await ctx.send("You can't kick me.")
        elif member == ctx.author:
            await ctx.send("You can't kick yourself.")
        else:
            await ctx.send(f"**{member}** has been kicked from the server.")
            channel = await self.config.guild(ctx.guild).channel()
            if channel and self.bot.get_channel(channel):
                fake_modlog = self.bot.get_channel(channel)
                case_id: int = await self.config.guild(ctx.guild).case_id()
                await self.config.guild(ctx.guild).case_id.set(case_id + 1)
                emoji = await self.config.guild(ctx.guild).kick_emoji()
                reason = reason if reason else "Not provided."
                embed = discord.Embed(
                    title=f"Case #{case_id} | Kick {emoji}", description=f"**Reason:** {reason}"
                )
                embed.set_author(name=f"{member} ({member.id})")
                embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})")
                embed.set_footer(text="just kidding lol")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                await fake_modlog.send(embed=embed)

    @commands.command(name="bam", aliases=["ben", "bon", "bean"])
    async def fake_ban(self, ctx, user: discord.User, *, reason: str = None):
        """Fake ban a user."""
        if user == ctx.me:
            await ctx.send("You can't ban me.")
        elif user == ctx.author:
            await ctx.send("You can't ban yourself.")
        else:
            await ctx.send(f"**{user}** has been banned from the server.")
            channel = await self.config.guild(ctx.guild).channel()
            if channel and self.bot.get_channel(channel):
                fake_modlog = self.bot.get_channel(channel)
                case_id: int = await self.config.guild(ctx.guild).case_id()
                await self.config.guild(ctx.guild).case_id.set(case_id + 1)
                emoji = await self.config.guild(ctx.guild).ban_emoji()
                reason = reason if reason else "Not provided."
                embed = discord.Embed(
                    title=f"Case #{case_id} | Ban {emoji}", description=f"**Reason:** {reason}"
                )
                embed.set_author(name=f"{user} ({user.id})")
                embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})")
                embed.set_footer(text="just kidding lol")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                await fake_modlog.send(embed=embed)
