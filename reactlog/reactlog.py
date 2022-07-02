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

from datetime import datetime

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import humanize_list


class ReactLog(commands.Cog):
    """
    Log when a reaction is added or removed!
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, 9517306284, True)
        self.config.register_guild(channel=None, reaction_add=False, reaction_remove=False)

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.2.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.group(aliases=["reactionlog"])
    @commands.admin()
    @commands.guild_only()
    async def reactlog(self, ctx):
        """ReactLog commands."""
        pass

    @reactlog.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the reactions logging channel."""
        if ctx.channel.permissions_for(channel.guild.me).send_messages:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(f"Set reaction log channel to: {channel.mention}")
        else:
            await ctx.send("Please grant me permission to send message in that channel first.")

    @reactlog.command(aliases=["reactionadd"])
    async def reactadd(self, ctx, on_or_off: bool):
        """Enable/disable logging when reactions added."""
        await self.config.guild(ctx.guild).reaction_add.set(on_or_off)
        if on_or_off:
            await ctx.send("I will log when reactions added.")
        else:
            await ctx.send("I won't log when reactions added.")

    @reactlog.command(aliases=["reactionremove"])
    async def reactremove(self, ctx, on_or_off: bool):
        """Enable/disable logging when reactions removed."""
        await self.config.guild(ctx.guild).reaction_remove.set(on_or_off)
        if on_or_off:
            await ctx.send("I will log when reactions removed.")
        else:
            await ctx.send("I won't log when reactions removed.")

    @reactlog.command(aliases=["settings"])
    @commands.bot_has_permissions(embed_links=True)
    async def showsettings(self, ctx):
        """Show the current settings."""
        channel = await self.config.guild(ctx.guild).channel()
        if channel:
            channel_mention = self.bot.get_channel(channel).mention
        else:
            channel_mention = "Not Set"
        reaction_add_status = await self.config.guild(ctx.guild).reaction_add()
        reaction_remove_status = await self.config.guild(ctx.guild).reaction_remove()
        if await ctx.embed_requested():
            embed = discord.Embed(title="Reaction Log Settings", color=await ctx.embed_color())
            embed.add_field(name="Channel", value=channel_mention, inline=True)
            embed.add_field(name="Log On Reaction Add", value=reaction_add_status, inline=True)
            embed.add_field(
                name="Log On Reaction Remove", value=reaction_remove_status, inline=True
            )
            embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format="png"))
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"**Reaction Log Settings for {ctx.guild.name}**\n"
                f"Channel: {channel_mention}\n"
                f"Log On Reaction Add: {reaction_add_status}\n"
                f"Log On Reaction Remove: {reaction_remove_status}"
            )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if reaction.count != 1:
            return
        await self.send_to_log(reaction.message, reaction.emoji, user, True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        if reaction.count != 0:
            return
        await self.send_to_log(reaction.message, reaction.emoji, user, False)

    async def send_to_log(self, message, emoji, user, added: bool) -> discord.Message:
        if not message.guild:
            return
        if not await self.config.guild(message.guild).reaction_remove():
            return
        if user.bot:
            return
        log = self.bot.get_channel(await self.config.guild(message.guild).channel())
        color = discord.Color.green() if added else discord.Color.red()
        embed = discord.Embed(color=color, timestamp=datetime.utcnow())
        embed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar_url)
        if isinstance(emoji, discord.Emoji):
            embed.description = (
                f"**Channel:** {message.channel.mention}\n"
                f"**Emoji:** {emoji.name} (ID: {emoji.id})\n"
                f"**Message:** [Jump to Message ►]({message.jump_url})"
            )
            url = emoji.url
        else:  # Default Emoji
            embed.description = (
                f"**Channel:** {message.channel.mention}\n"
                f"**Emoji:** {emoji}\n"
                f"**Message:** [Jump to Message ►]({message.jump_url})"
            )
            # https://github.com/flapjax/FlapJack-Cogs/blob/red-v3-rewrites/bigmoji/bigmoji.py#L69-L93
            chars = [str(hex(ord(c)))[2:] for c in emoji]
            if len(chars) == 2:
                if "fe0f" in chars:
                    chars.remove("fe0f")
            if "20e3" in chars:
                chars.remove("fe0f")
            url = f"https://twemoji.maxcdn.com/2/72x72/{'-'.join(chars)}.png"
        embed.set_thumbnail(url=url)
        a_or_r = "Added" if added else "Removed"
        embed.set_footer(text=f"Reaction {a_or_r} | #{message.channel.name}")
        await log.send(embed=embed)
