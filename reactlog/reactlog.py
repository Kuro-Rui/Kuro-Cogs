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

from collections import defaultdict
from typing import DefaultDict, List, Optional, Tuple, Union

import discord
import kuroutils
from discord.ext import tasks
from redbot.core import Config, app_commands, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.menus import menu

Channel = Union[discord.TextChannel, discord.VoiceChannel, discord.Thread]


class ReactLog(kuroutils.Cog):
    """Log when reactions are added or removed."""

    __author__ = ["Kuro"]
    __version__ = "0.2.2"

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
        self.cache: DefaultDict[int, List[discord.Embed]] = defaultdict(lambda: [])
        self.send_grouped_reaction_embeds.start()

    @tasks.loop(seconds=10)
    async def send_grouped_reaction_embeds(self):
        if not await self._config.grouped():
            return
        # This is to prevent RuntimeError
        # Since we can't assign to the dictionary while being iterated, we have to copy it.
        for guild_id, embeds in self.cache.copy().items():
            if not embeds:
                continue
            if not (guild := self.bot.get_guild(guild_id)):
                del self.cache[guild_id]
                continue
            if not (channel_id := await self._config.guild(guild).channel()):
                continue
            if not (channel := guild.get_channel_or_thread(channel_id)):
                continue
            await channel.send(embeds=self.cache[guild_id][:10])
            self.cache[guild_id] = self.cache[guild_id][10:]

    @send_grouped_reaction_embeds.before_loop
    async def before_send_grouped_embeds(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        super().cog_unload()
        self.send_grouped_reaction_embeds.stop()

    @commands.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.hybrid_group(aliases=["reactionlog"])
    async def reactlog(self, ctx: commands.Context):
        """Reaction logging configuration commands."""
        pass

    @commands.is_owner()
    @reactlog.command(with_app_command=False)
    async def grouped(self, ctx: commands.Context, toggle: Optional[bool] = None):
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
    async def blacklist(self, ctx: commands.Context):
        """Add/remove a member from reactlog blacklist."""
        blacklist = await self._config.guild(ctx.guild).blacklist()
        if not blacklist:
            description = "No member is being blacklisted."
        else:
            description = "\n".join(
                f"{self.bot.get_user(member_id).mention}" for member_id in blacklist
            )

        embeds = []
        for page in pagify(description, page_length=1024):
            embed = discord.Embed(
                color=await ctx.embed_color(), title="Reactlog Blacklist", description=page
            )
            embed.set_footer(
                text=(
                    "To add/remove member from blacklist, "
                    f"run {ctx.clean_prefix}reactlog blacklist add/remove <member>"
                )
            )
            embeds.append(embed)
        await menu(ctx, embeds, timeout=60)

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
        self,
        ctx: commands.Context,
        channel: Optional[Union[discord.TextChannel, discord.Thread]] = None,
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
    async def ignore(self, ctx: commands.Context):
        """Add/remove a channel from reactlog ignore list."""
        ignored = await self._config.guild(ctx.guild).ignored()
        if not ignored:
            description = "No channel is being ignored."
        else:
            description = "\n".join(
                f"{self.bot.get_channel(channel_id).mention} (ID: {channel_id})"
                for channel_id in ignored
            )

        embeds = []
        for page in pagify(description, page_length=1024):
            embed = discord.Embed(
                color=await ctx.embed_color(), title="ReactLog Ignore List", description=page
            )
            embed.set_footer(
                text=(
                    "To add/remove a channel from ignore list, "
                    f"run {ctx.clean_prefix}reactlog ignore add/remove <channel>"
                )
            )
            embeds.append(embed)
        await menu(ctx, embeds, timeout=60)

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
    async def reactadd(self, ctx: commands.Context, toggle: Optional[bool] = None):
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
    async def reactdel(self, ctx: commands.Context, toggle: Optional[bool] = None):
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
    async def logall(self, ctx: commands.Context, toggle: Optional[bool] = None):
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
        config = await self._config.guild(ctx.guild).all()
        if channel := config["channel"]:
            channel_mention = self.bot.get_channel(channel).mention
        else:
            channel_mention = "Not Set"
        if await ctx.embed_requested():
            embed = discord.Embed(title="Reaction Log Settings", color=await ctx.embed_color())
            embed.add_field(name="Log On Reaction Add?", value=config["react_add"], inline=True)
            embed.add_field(
                name="Log On Reaction Remove?", value=config["react_remove"], inline=True
            )
            embed.add_field(name="Log All Reactions?", value=config["log_all"], inline=True)
            embed.add_field(name="Channel", value=channel_mention, inline=True)
            embed.set_footer(text=ctx.guild.name, icon_url=getattr(ctx.guild.icon, "url", None))
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"**Reaction Log Settings for {ctx.guild.name}**\n"
                f"Channel: {channel_mention}\n"
                f"Log On Reaction Add: {config['react_add']}\n"
                f"Log On Reaction Remove: {config['react_add']}\n"
                f"Log All Reactions: {config['log_all']}"
            )

    async def _check(self, user: discord.Member, channel: Channel) -> bool:
        if user.bot:
            return False
        guild = channel.guild
        config = await self._config.guild(guild).all()
        if not (log_channel := config["channel"]):
            return False
        if not guild.get_channel_or_thread(log_channel):
            return False
        if channel.id in config["ignored"]:
            return False
        if user.id in config["blacklist"]:
            return False
        return True

    async def _get_reaction_and_user(
        self, payload: discord.RawReactionActionEvent
    ) -> Tuple[Optional[discord.Reaction], Optional[discord.Member]]:
        channel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return None, None
        message = await channel.fetch_message(payload.message_id)
        if not message:
            return None, None
        reaction = discord.utils.find(
            lambda e: str(e.emoji) == str(payload.emoji), message.reactions
        )
        return reaction, channel.guild.get_member(payload.user_id)

    async def make_embed(
        self,
        emoji: discord.PartialEmoji,
        message: discord.Message,
        user: discord.Member,
        *,
        added: bool,
    ) -> None:
        if emoji.is_custom_emoji():
            description = (
                f"**Channel:** {message.channel.mention}\n"
                f"**Emoji:** {emoji.name} (ID: {emoji.id})"
            )
            url = emoji.url
        else:
            description = f"**Channel:** {message.channel.mention}\n**Emoji:** {emoji}"
            # https://github.com/flapjax/FlapJack-Cogs/blob/red-v3-rewrites/bigmoji/bigmoji.py#L69-L93
            chars = [str(hex(ord(c)))[2:] for c in str(emoji)]
            if len(chars) == 2 and "fe0f" in chars or "20e3" in chars:
                chars.remove("fe0f")
            url = f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{'-'.join(chars)}.png"

        color = discord.Color.green() if added else discord.Color.red()
        embed = discord.Embed(
            color=color, description=description, timestamp=discord.utils.utcnow()
        )
        embed.set_author(name=f"{user} ({user.id})", icon_url=user.display_avatar.url)
        embed.set_thumbnail(url=url)
        embed.set_footer(
            text=f"Reaction {'Added' if added else 'Removed'} | #{message.channel.name}"
        )
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
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if not (guild_id := payload.guild_id):
            return
        reaction, user = await self._get_reaction_and_user(payload)
        if not all((reaction, user)):
            return
        config = await self._config.guild_from_id(guild_id).all()
        if not (
            config["react_add"]
            and await self._check(user, reaction.message.channel)
            and (config["log_all"] or reaction.count == 1)
        ):
            return
        await self.make_embed(payload.emoji, reaction.message, user, added=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if not (guild_id := payload.guild_id):
            return
        # If reaction is None, it means there are no reactions with that emoji (reaction.count == 0)
        reaction, user = await self._get_reaction_and_user(payload)
        if not user:
            return
        if not (channel := self.bot.get_channel(payload.channel_id)):
            return
        config = await self._config.guild_from_id(guild_id).all()
        if not (
            config["react_remove"]
            and await self._check(user, channel)
            and (config["log_all"] or not reaction)
        ):
            return
        if not (message := await channel.fetch_message(payload.message_id)):
            return
        await self.make_embed(payload.emoji, message, user, added=False)
