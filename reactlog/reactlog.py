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

import re
from typing import Union

import discord
import kuroutils
from discord.ext import tasks
from redbot.core import Config, app_commands, commands
from redbot.core.bot import Red

Channel = Union[discord.TextChannel, discord.VoiceChannel, discord.Thread]


class ReactLog(kuroutils.Cog):
    """Log when reactions are added or removed."""

    __author__ = ["Kuro"]
    __version__ = "0.0.6"

    def __init__(self, bot: Red):
        super().__init__(bot)
        self._config = Config.get_conf(self, 9517306284, True)
        self._config.register_global(grouped=False)
        self._config.register_guild(
            blacklist=[],
            channel=None,
            ignored=[],
            log_all=False,
            react_add=False,
            react_remove=False,
        )
        self.cache = kuroutils.DefaultDict(lambda: [])
        self.send_grouped_reaction_embeds.start()

    @tasks.loop(seconds=10)
    async def send_grouped_reaction_embeds(self):
        if not await self._config.grouped():
            return
        # This is to prevent RuntimeError
        # Since you can't assign to the dictionary being iterated, we have to copy it.
        for guild_id, embeds in self.cache.copy().items():
            if not embeds:
                del self.cache[guild_id]
                continue
            if not (guild := self.bot.get_guild(guild_id)):
                del self.cache[guild_id]
                continue
            if not (channel_id := await self._config.guild(guild).channel()):
                continue
            if not (channel := guild.get_channel_or_thread(channel_id)):
                continue
            embeds = self.cache[guild_id][:10]
            self.cache[guild_id] = self.cache[guild_id][10:]
            await channel.send(embeds=embeds)

    @send_grouped_reaction_embeds.before_loop
    async def before_send_grouped_embeds(self):
        await self.bot.wait_until_ready()

    @commands.admin()
    @commands.guild_only()
    @commands.hybrid_group(aliases=["reactionlog"])
    async def reactlog(self, ctx: commands.Context):
        """Reaction logging configuration commands."""
        pass

    @reactlog.command(with_app_command=False)
    @app_commands.describe(time="The time in seconds to group reactions.")
    async def grouped(self, ctx: commands.Context, toggle: bool = None):
        """
        Set whether to group reaction logging embeds.

        This is useful if your bot is in many servers and has a lot of users.
        """
        current = await self._config.grouped()
        if toggle is None:
            await self._config.grouped.set(not current)
        else:
            await self._config.grouped.set(toggle)

        if await self._config.grouped():
            await ctx.send("I will group reaction logging embeds from now.")
            return
        await ctx.send("I won't group reaction logging embeds from now.")

    @reactlog.group(aliases=["bl"], invoke_without_command=True)
    @commands.mod_or_permissions(administrator=True)
    async def blacklist(self, ctx: commands.Context):
        """Add/remove a member from reactlog blacklist."""
        embed = discord.Embed(title="Reactlog Blacklist", color=await ctx.embed_color())
        async with self._config.guild(ctx.guild).blacklist() as blacklist:
            if not blacklist:
                embed.description = "No member is being blacklisted."
            else:
                embed.description = "\n".join(
                    f"{self.bot.get_user(member_id).mention}" for member_id in blacklist
                )
        embed.set_footer(
            text=f"To add/remove member from blacklist, use {ctx.clean_prefix}reactlog blacklist add/remove <member>"
        )
        await ctx.send(embed=embed)

    @blacklist.command(name="add")
    @app_commands.describe(member="The member to add to reactlog blacklist.")
    async def blacklist_add(self, ctx: commands.Context, member: discord.Member):
        """Add a member to reactlog blacklist."""
        async with self._config.guild(ctx.guild).blacklist() as blacklist:
            if member.id in blacklist:
                await ctx.send(f"{member} is already in the blacklist.")
                return
            blacklist.append(member.id)
        await ctx.send(f"{member} has been added to the blacklist.")

    @blacklist.command(name="remove")
    @app_commands.describe(member="The member to remove from reactlog blacklist.")
    async def blacklist_remove(self, ctx: commands.Context, member: discord.Member):
        """Remove a member from reactlog blacklist."""
        async with self._config.guild(ctx.guild).blacklist() as blacklist:
            if member.id not in blacklist:
                await ctx.send(f"{member} is not in the blacklist.")
                return
            blacklist.remove(member.id)
        await ctx.send(f"{member} has been removed from the blacklist.")

    @reactlog.command()
    @app_commands.describe(channel="The channel to log reactions to.")
    async def channel(
        self, ctx: commands.Context, channel: Union[discord.TextChannel, discord.Thread] = None
    ):
        """Set the reactions logging channel."""
        if not channel:
            await self._config.guild(ctx.guild).channel.clear()
            await ctx.send("Reaction logging channel has been unset.")
            return
        if not ctx.channel.permissions_for(channel.guild.me).send_messages:
            await ctx.send("Please grant me permission to send message in that channel first.")
            return
        await self._config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Reaction logging channel has been set to: {channel.mention}")

    @reactlog.group(invoke_without_command=True)
    @commands.mod_or_permissions(administrator=True)
    async def ignore(self, ctx: commands.Context):
        """Add/remove a channel from reactlog ignore list."""
        embed = discord.Embed(title="Reactlog Ignore List", color=await ctx.embed_color())
        async with self._config.guild(ctx.guild).ignored() as ignored:
            if not ignored:
                embed.description = "No channel is being ignored."
            else:
                embed.description = "\n".join(
                    f"{self.bot.get_channel(channel_id).mention} (ID: {channel_id})"
                    for channel_id in ignored
                )
        embed.set_footer(
            text=f"To add/remove channel from ignore list, use {ctx.clean_prefix}reactlog ignore add/remove <channel>"
        )
        await ctx.send(embed=embed)

    @ignore.command(name="add")
    @app_commands.describe(channel="The channel to add to reactlog ignore list.")
    async def ignore_add(self, ctx: commands.Context, channel: Channel):
        """Add a channel to reactlog ignore list."""
        async with self._config.guild(ctx.guild).ignored() as ignored:
            if channel.id in ignored:
                await ctx.send(f"{channel.mention} is already in the ignore list.")
                return
            ignored.append(channel.id)
        await ctx.send(f"{channel.mention} has been added to the ignore list.")

    @ignore.command(name="remove")
    @app_commands.describe(channel="The channel to remove from reactlog ignore list.")
    async def ignore_remove(self, ctx: commands.Context, channel: Channel):
        """Remove a channel from reactlog ignore list."""
        async with self._config.guild(ctx.guild).ignored() as ignored:
            if channel.id not in ignored:
                await ctx.send(f"{channel.mention} is not in the ignore list.")
                return
            ignored.remove(channel.id)
        await ctx.send(f"{channel.mention} has been removed from the ignore list.")

    @reactlog.command()
    @app_commands.describe(toggle="True or False")
    async def reactadd(self, ctx: commands.Context, toggle: bool = None):
        """Enable/disable logging when reactions added."""
        current = await self._config.guild(ctx.guild).react_add()
        if toggle is None:
            await self._config.guild(ctx.guild).react_add.set(not current)
        else:
            await self._config.guild(ctx.guild).react_add.set(toggle)

        if await self._config.guild(ctx.guild).react_add():
            await ctx.send("I will log when reactions added.")
            return
        await ctx.send("I won't log when reactions added.")

    @reactlog.command()
    @app_commands.describe(toggle="True or False")
    async def reactdel(self, ctx: commands.Context, toggle: bool = None):
        """Enable/disable logging when reactions removed."""
        current = await self._config.guild(ctx.guild).react_remove()
        if toggle is None:
            await self._config.guild(ctx.guild).react_remove.set(not current)
        else:
            await self._config.guild(ctx.guild).react_remove.set(toggle)

        if await self._config.guild(ctx.guild).react_remove():
            await ctx.send("I will log when reactions removed.")
            return
        await ctx.send("I won't log when reactions removed.")

    @reactlog.command()
    @app_commands.describe(toggle="True or False")
    async def logall(self, ctx: commands.Context, toggle: bool = None):
        """
        Set whether to log all reactions or not.

        If enabled, all reactions will be logged.
        If disabled, only first added or last removed reactions will be logged.

        Just a gentle reminder, it would be spammy if enabled.
        """
        current = await self._config.guild(ctx.guild).log_all()
        if toggle is None:
            await self._config.guild(ctx.guild).log_all.set(not current)
        else:
            await self._config.guild(ctx.guild).log_all.set(toggle)

        if await self._config.guild(ctx.guild).log_all():
            await ctx.send("I will log all reactions from now.")
            return
        await ctx.send("I won't log all reactions from now.")

    @reactlog.command()
    async def settings(self, ctx: commands.Context):
        """Show current reaction log settings."""
        channel = await self._config.guild(ctx.guild).channel()
        if channel:
            channel_mention = self.bot.get_channel(channel).mention
        else:
            channel_mention = "Not Set"
        react_add_status = await self._config.guild(ctx.guild).react_add()
        react_remove_status = await self._config.guild(ctx.guild).react_remove()
        log_all_status = await self._config.guild(ctx.guild).log_all()
        if await ctx.embed_requested():
            embed = discord.Embed(title="Reaction Log Settings", color=await ctx.embed_color())
            embed.add_field(name="Log On Reaction Add?", value=react_add_status, inline=True)
            embed.add_field(name="Log On Reaction Remove?", value=react_remove_status, inline=True)
            embed.add_field(name="Log All Reactions?", value=log_all_status, inline=True)
            embed.add_field(name="Channel", value=channel_mention, inline=True)
            embed.set_footer(text=ctx.guild.name, icon_url=getattr(ctx.guild.icon, "url", None))
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"**Reaction Log Settings for {ctx.guild.name}**\n"
                f"Channel: {channel_mention}\n"
                f"Log On Reaction Add: {react_add_status}\n"
                f"Log On Reaction Remove: {react_remove_status}\n"
                f"Log All Reactions: {log_all_status}"
            )

    async def _check(self, member: discord.Member, message: discord.Message) -> bool:
        if member.bot:
            return False
        if not (guild := message.guild):
            return False
        if not (log_channel := await self._config.guild(guild).channel()):
            return False
        channel = message.channel
        if channel.id in await self._config.guild(guild).ignored():
            return False
        if member.id in await self._config.guild(message.guild).blacklist():
            return False
        if not guild.get_channel_or_thread(log_channel):
            self._log.info(
                f"Channel or Thread with ID {log_channel} not found in {guild} (ID: {guild.id}), ignoring."
            )
            return False
        return True

    async def make_or_send_embed(
        self, message: discord.Message, emoji: str, user: discord.Member, *, added: bool
    ) -> discord.Embed:
        # https://github.com/Rapptz/discord.py/blob/462ba84/discord/ext/commands/converter.py#L700
        match = re.match(r"<a?:([a-zA-Z0-9\_]{1,32}):([0-9]{15,20})>$", emoji)
        if match:
            description = (
                f"**Channel:** {message.channel.mention}\n"
                f"**Emoji:** {match.group(1)} (ID: {match.group(2)})"
            )
            url = f"https://cdn.discordapp.com/emojis/{match.group(2)}"
            url += ".gif" if emoji.startswith("<a") else ".png"
        else:  # Default Emoji
            description = f"**Channel:** {message.channel.mention}\n**Emoji:** {emoji.strip(':')}"
            # https://github.com/flapjax/FlapJack-Cogs/blob/red-v3-rewrites/bigmoji/bigmoji.py#L69-L93
            chars = [str(hex(ord(c)))[2:] for c in emoji]
            if len(chars) == 2:
                if "fe0f" in chars:
                    chars.remove("fe0f")
            if "20e3" in chars:
                chars.remove("fe0f")
            url = f"https://twemoji.maxcdn.com/v/14.0.2/72x72/{'-'.join(chars)}.png"
        color = discord.Color.green() if added else discord.Color.red()
        embed = discord.Embed(
            description=description, color=color, timestamp=discord.utils.utcnow()
        )
        embed.set_author(name=f"{user} ({user.id})", icon_url=user.display_avatar.url)
        embed.set_thumbnail(url=url)
        added_or_removed = "Added" if added else "Removed"
        embed.set_footer(text=f"Reaction {added_or_removed} | #{message.channel.name}")
        if await self._config.grouped():
            embed.description += f"\n**Message:** [Jump to Message ►]({message.jump_url})"
            self.cache[message.guild.id].append(embed)
            return
        view = discord.ui.View()
        button = discord.ui.Button(
            style=discord.ButtonStyle.link, label="Jump to Message", url=message.jump_url
        )
        view.add_item(button)
        channel_id = await self._config.guild(message.guild).channel()
        channel = message.guild.get_channel_or_thread(channel_id)
        await channel.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        if not await self._config.guild(message.guild).react_add():
            return
        if not await self._check(user, message):
            return
        log_all = await self._config.guild(message.guild).log_all()
        if not log_all and reaction.count != 1:
            return
        await self.make_or_send_embed(message, str(reaction.emoji), user, added=True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        if not await self._config.guild(message.guild).react_remove():
            return
        if not await self._check(user, message):
            return
        log_all = await self._config.guild(message.guild).log_all()
        if not log_all and reaction.count != 0:
            return
        await self.make_or_send_embed(message, str(reaction.emoji), user, added=False)
