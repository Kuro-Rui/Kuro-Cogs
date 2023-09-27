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
from red_commons.logging import RedTraceLogger
from redbot.core import Config, commands
from redbot.core.bot import Red

Channel = Union[discord.TextChannel, discord.VoiceChannel, discord.Thread]


class Events:
    def __init__(self):
        self.bot: Red
        self.cache: kuroutils.DefaultDict
        self._config: Config
        self._log: RedTraceLogger

    async def _check(self, member: discord.Member, message: discord.Message) -> bool:
        if member.bot:
            return
        if not (guild := message.guild):
            return
        if not (log_channel := await self._config.guild(guild).channel()):
            return
        channel = message.channel
        if channel.id in await self._config.guild(guild).ignored():
            return
        if member.id in await self._config.guild(message.guild).blacklist():
            return
        if not guild.get_channel_or_thread(log_channel):
            self._log.info(
                f"Channel or Thread with ID {log_channel} not found in {guild} (ID: {guild.id}), ignoring."
            )
            return

    async def make_embed(
        self, message: discord.Message, emoji: str, user: discord.Member, *, added: bool
    ) -> None:
        # https://github.com/Rapptz/discord.py/blob/462ba84/discord/ext/commands/converter.py#L700
        match = re.match(r"<a?:([a-zA-Z0-9\_]{1,32}):([0-9]{15,20})>$", emoji)
        if match:
            description = (
                f"**Channel:** {message.channel.mention}\n"
                f"**Emoji:** {match.group(1)} (ID: {match.group(2)})\n"
                f"**Message:** [Jump to Message ►]({message.jump_url})"
            )
            url = f"https://cdn.discordapp.com/emojis/{match.group(2)}"
            url += ".gif" if emoji.startswith("<a") else ".png"
        else:  # Default Emoji
            description = (
                f"**Channel:** {message.channel.mention}\n"
                f"**Emoji:** {emoji.strip(':')}\n"
                f"**Message:** [Jump to Message ►]({message.jump_url})"
            )
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
        self.cache[message.guild.id].append(embed)

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
        await self.make_embed(message, str(reaction.emoji), user, added=True)

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
        await self.make_embed(message, str(reaction.emoji), user, added=False)
