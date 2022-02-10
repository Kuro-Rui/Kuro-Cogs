import datetime

import discord
from redbot.core import commands
from redbot.core.config import Config


class ReactLog(commands.Cog):
    """
    Log when a reaction is added or removed!
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, 9517306284, True)
        self.config.register_guild(channel=None, reaction_add=False, reaction_remove=False)

    @commands.group(aliases=["reactlogs", "reactionlog", "reactionlogs"])
    @commands.admin()
    @commands.guild_only()
    async def reactlog(self, ctx):
        """ReactLog commands."""
        pass

    @reactlog.group()
    async def set(self, ctx):
        """ReactLog settings."""
        pass

    @set.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the reactions logging channel."""
        if ctx.channel.permissions_for(channel.guild.me).send_messages == True:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(f"Set reaction log channel to: {channel.mention}")
        else:
            await ctx.send("Please grant me permission to send message in that channel first.")

    @set.command(aliases=["reactionadd"])
    async def reactadd(self, ctx, on_or_off: bool):
        """Enable/disable logging when reactions added."""
        await self.config.guild(ctx.guild).reaction_add.set(on_or_off)
        if on_or_off == True:
            await ctx.send("I will log when reactions added.")
        else:
            await ctx.send("I won't log when reactions added.")

    @set.command(aliases=["reactionremove"])
    async def reactremove(self, ctx, on_or_off: bool):
        """Enable/disable logging when reactions removed."""
        await self.config.guild(ctx.guild).reaction_remove.set(on_or_off)
        if on_or_off == True:
            await ctx.send("I will log when reactions removed.")
        else:
            await ctx.send("I won't log when reactions removed.")

    @reactlog.command(aliases=["settings"])
    @commands.bot_has_permissions(embed_links=True)
    async def showsettings(self, ctx):
        """Show the current settings."""
        channel = await self.config.guild(ctx.guild).channel()
        reaction_add_status = await self.config.guild(ctx.guild).reaction_add()
        reaction_remove_status = await self.config.guild(ctx.guild).reaction_remove()
        embed = discord.Embed(title="Reaction Log Settings", color=await ctx.embed_color())
        embed.add_field(name="Channel", value=f"<#{channel}>", inline=True)
        embed.add_field(name="Log On Reaction Add", value=reaction_add_status, inline=True)
        embed.add_field(name="Log On Reaction Remove", value=reaction_remove_status, inline=True)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format="png"))
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        log_channel = await self.config.guild(user.guild).channel()
        log = self.bot.get_channel(log_channel)
        message = reaction.message
        channel = message.channel
        emoji = reaction.emoji
        if await self.config.guild(user.guild).reaction_add():
            if message.author.bot == False:
                embed = discord.Embed(color=discord.Color.green())
                embed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar_url)
                embed.description = (
                    f"**Channel:** {channel.mention}\n"
                    f"**Emoji:** {emoji.name} (ID: {emoji.id})\n"
                    f"**Message:** [Jump to Message ►]({message.jump_url})"
                )
                embed.set_thumbnail(url=emoji.url)
                embed.set_footer(text=f"Reaction Added | #{channel.name}")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                await log.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        log_channel = await self.config.guild(user.guild).channel()
        log = self.bot.get_channel(log_channel)
        message = reaction.message
        channel = message.channel
        emoji = reaction.emoji
        if await self.config.guild(user.guild).reaction_remove():
            if message.author.bot == False:
                embed = discord.Embed(color=discord.Color.red())
                embed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar_url)
                embed.description = (
                    f"**Channel:** {channel.mention}\n"
                    f"**Emoji:** {emoji.name} (ID: {emoji.id})\n"
                    f"**Message:** [Jump to Message ►]({reaction.message.jump_url})"
                )
                embed.set_thumbnail(url=emoji.url)
                embed.set_footer(text=f"Reaction Removed | #{channel.name}")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                await log.send(embed=embed)