import asyncio
import datetime
from typing import Union

import discord
from redbot.core import Config, commands
from redbot.core.utils.predicates import MessagePredicate

# Inspired by Jeff (https://github.com/Noa-DiscordBot/Noa-Cogs/blob/main/fakemod/fakemod.py)
class FakeMod(commands.Cog):
    """Fake Moderation Tools."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 9863948134, True)
        self.config.register_guild(
            channel=None, 
            case_id=1,
            worn_emoji="\N{HEAVY HEART EXCLAMATION MARK ORNAMENT}\N{VARIATION SELECTOR-16}", 
            myut_emoji="\N{FACE WITH FINGER COVERING CLOSED LIPS}", 
            kik_emoji="\N{HIGH-HEELED SHOE}", 
            ben_emoji="\N{COLLISION SYMBOL}"
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
            if ctx.channel.permissions_for(channel.guild.me).send_messages == True:
                await self.config.guild(ctx.guild).channel.set(channel.id)
                await ctx.send(f"Fake mod events will be sent to {channel.mention}.")
            else:
                await ctx.send("Please grant me permission to send message in that channel first.")
        else:
            await self.config.guild(ctx.guild).channel.clear()
            await ctx.send("Fake mod log deactivated.")

    @fakemodlogset.command()
    async def emoji(self, ctx, action: str = None, emoji: str = None):
        """Set an emoji for a fake mod action."""

        guild = ctx.guild

        worn_emoji = await self.config.guild(guild).worn_emoji()
        myut_emoji = await self.config.guild(guild).myut_emoji()
        kik_emoji = await self.config.guild(guild).kik_emoji()
        ben_emoji = await self.config.guild(guild).ben_emoji()

        current_settings = (
            "Current Settings:\n"
            "`Worn` : {}\n"
            "`Myut` : {}\n"
            "`Kik`  : {}\n"
            "`Ben`  : {}\n"
        ).format(worn_emoji, myut_emoji, kik_emoji, ben_emoji)

        if action is None:
            await ctx.send_help()
            await ctx.send(current_settings)
        else:
            action = action.lower()
            casetype = ["worn", "myut", "kik", "ben"]
            if action not in casetype:
                await ctx.send(
                    "I can't find that action. You can choose either `worn`, `myut`, `kik`, and `ben`."
                )
            else:
                if action == "worn" and emoji != None:
                    try:
                        await ctx.message.add_reaction(emoji)
                        await self.config.guild(guild).worn_emoji.set(emoji)
                        await ctx.send("Emoji for `worn` has been set.")
                    except:
                        await ctx.send("I can't use that emoji.")
                elif action == "worn" and emoji == None:
                    await self.config.guild(guild).worn_emoji.set(
                        "\N{HEAVY HEART EXCLAMATION MARK ORNAMENT}\N{VARIATION SELECTOR-16}"
                    )
                    await ctx.send("The emoji has been reset.")
                elif action == "myut" and emoji != None:
                    try:
                        await ctx.message.add_reaction(emoji)
                        await self.config.guild(guild).myut_emoji.set(emoji)
                        await ctx.send("Emoji for `myut` has been set.")
                    except:
                        await ctx.send("I can't use that emoji.")
                elif action == "myut" and emoji == None:
                    await self.config.guild(guild).myut_emoji.set("\N{FACE WITH FINGER COVERING CLOSED LIPS}")
                    await ctx.send("The emoji has been reset.")
                elif action == "kik" and emoji != None:
                    try:
                        await ctx.message.add_reaction(emoji)
                        await self.config.guild(guild).kik_emoji.set(emoji)
                        await ctx.send("Emoji for `kik` has been set.")
                    except:
                        await ctx.send("I can't use that emoji.")
                elif action == "kik" and emoji == None:
                    await self.config.guild(guild).kik_emoji.set("\N{HIGH-HEELED SHOE}")
                    await ctx.send("The emoji has been reset.")
                elif action == "ben" and emoji != None:
                    try:
                        await ctx.message.add_reaction(emoji)
                        await self.config.guild(guild).ben_emoji.set(emoji)
                        await ctx.send("Emoji for `ben` has been set.")
                    except:
                        await ctx.send("I can't use that emoji.")
                elif action == "ben" and emoji == None:
                    await self.config.guild(guild).ben_emoji.set("\N{COLLISION SYMBOL}")
                    await ctx.send("The emoji has been reset.")

    @fakemodlogset.command()
    async def resetcases(self, ctx):
        """Reset all fake modlog cases in this server."""
        await ctx.send("Would you like to reset all fake modlog cases in this server? (yes/no)")
        try:
            pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
            await ctx.bot.wait_for("message", check=pred, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        if pred.result:
            await self.config.guild(ctx.guild).case_id.set(1)
            await ctx.send("Cases have been reset.")
        else:
            await ctx.send("No changes have been made.")

    @commands.command()
    async def worn(self, ctx, user: Union[discord.User, discord.Member], reason: str = None):
        """Worn the user for the specified reason."""
        if user == ctx.me:
            await ctx.send("You can't worn me.")
        elif user == ctx.author:
            await ctx.send("You can't worn yourself.")
        else:
            await ctx.tick()
            channel = await self.config.guild(ctx.guild).channel()
            fake_modlog = self.bot.get_channel(channel)
            case_id: int = await self.config.guild(ctx.guild).case_id()
            await self.config.guild(ctx.guild).case_id.set(case_id + 1)
            emoji = await self.config.guild(ctx.guild).worn_emoji()
            reason = reason if reason else "Not provided."
            embed = discord.Embed(title=f"Case #{case_id} | Worn {emoji}", description=f"**Reason:** {reason}")
            embed.set_author(name=f"{user} ({user.id})")
            embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})")
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await fake_modlog.send(embed=embed)

    @commands.command()
    async def myut(self, ctx, user: Union[discord.User, discord.Member], *, reason: str = None):
        """Myut a user."""
        if user == ctx.me:
            await ctx.send("You can't myut me.")
        elif user == ctx.author:
            await ctx.send("You can't myut yourself.")
        else:
            await ctx.send(f"{user} has been myuted in this server.")
            channel = await self.config.guild(ctx.guild).channel()
            fake_modlog = self.bot.get_channel(channel)
            case_id: int = await self.config.guild(ctx.guild).case_id()
            await self.config.guild(ctx.guild).case_id.set(case_id + 1)
            emoji = await self.config.guild(ctx.guild).myut_emoji()
            reason = reason if reason else "Not provided."
            embed = discord.Embed(title=f"Case #{case_id} | Myut {emoji}", description=f"**Reason:** {reason}")
            embed.set_author(name=f"{user} ({user.id})")
            embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})")
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await fake_modlog.send(embed=embed)

    @commands.command()
    async def kik(self, ctx, user: Union[discord.User, discord.Member], *, reason: str = None):
        """Kik a user."""
        if user == ctx.me:
            await ctx.send("You can't kik me.")
        elif user == ctx.author:
            await ctx.send("You can't kik yourself.")
        else:
            await ctx.send(f"**{user}** has been kikked from the server.")
            channel = await self.config.guild(ctx.guild).channel()
            fake_modlog = self.bot.get_channel(channel)
            case_id: int = await self.config.guild(ctx.guild).case_id()
            await self.config.guild(ctx.guild).case_id.set(case_id + 1)
            emoji = await self.config.guild(ctx.guild).kik_emoji()
            reason = reason if reason else "Not provided."
            embed = discord.Embed(title=f"Case #{case_id} | Kik {emoji}", description=f"**Reason:** {reason}")
            embed.set_author(name=f"{user} ({user.id})")
            embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})")
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await fake_modlog.send(embed=embed)

    @commands.command()
    async def ben(self, ctx, user: Union[discord.User, discord.Member], *, reason: str = None):
        """Ben a user."""
        if user == ctx.me:
            await ctx.send("You can't ben me.")
        elif user == ctx.author:
            await ctx.send("You can't ben yourself.")
        else:
            await ctx.send(f"**{user}** has been benned from the server.")
            channel = await self.config.guild(ctx.guild).channel()
            fake_modlog = self.bot.get_channel(channel)
            case_id: int = await self.config.guild(ctx.guild).case_id()
            await self.config.guild(ctx.guild).case_id.set(case_id + 1)
            emoji = await self.config.guild(ctx.guild).ben_emoji()
            reason = reason if reason else "Not provided."
            embed = discord.Embed(title=f"Case #{case_id} | Ben {emoji}", description=f"**Reason:** {reason}")
            embed.set_author(name=f"{user} ({user.id})")
            embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})")
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await fake_modlog.send(embed=embed)