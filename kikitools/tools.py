# Stolen some from https://github.com/kaogurai/cogs/blob/master/kaotools/kaotools.py (Ty alec)

import contextlib
import random
import re
import sys
import time
import urllib
from copy import copy

import aiohttp
import discord
import dislash
from dislash.interactions import ActionRow, Button, ButtonStyle

import redbot
from redbot.cogs.downloader.converters import InstalledCog
from redbot.core import Config, commands
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import box, humanize_list, pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

from zalgo_text import zalgo

SUPPORT_SERVER = "https://discord.gg/Zef3pD8Yt5"


class KikiTools(commands.Cog):
    """
    Some tools for Kiki✨ that I hope useful.
    """

    __version__ = "1.1.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=10023)
        default_global = {
            "blacklist": [],
            "whitelist": [],
        }
        self.config.register_global(**default_global)
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        del self.bot._connection.parsers["INTERACTION_CREATE"]
        self.bot.loop.create_task(self.session.close())

    def format_help_for_context(self, ctx):
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        if not message.channel.permissions_for(message.guild.me).send_messages:
            return
        if await self.bot.allowed_by_whitelist_blacklist(who=message.author) is False:
            return
        if not re.compile(rf"^<@!?{self.bot.user.id}>$").match(message.content):
            return
        prefixes = await self.bot.get_prefix(message.channel)
        if f"<@!{self.bot.user.id}> " in prefixes:
            prefixes.remove(f"<@!{self.bot.user.id}> ")
        sorted_prefixes = sorted(prefixes, key=len)
        if len(sorted_prefixes) > 500:
            return
        d = (
            f"My prefixes in this server are {humanize_list(prefixes)}\n"
            f"You can type `{sorted_prefixes[0]}help` to view all commands!"
        )
        embed = discord.Embed(
            title="**Hey There!** <a:Kiki:922371688635707412>",
            colour=await self.bot.get_embed_colour(message.channel),
            description=d
        )
        await message.channel.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def poll(self, ctx, *, question: str):
        """
        Create a simple poll.
        """
        if len(question) > 2000:
            await ctx.send("That question is too long.")
            return
        message = await ctx.send(f"**{ctx.author} asks:** " + question)
        await message.add_reaction("<:LalaOk:922835155712884777>")
        await message.add_reaction("<:KikiNo:922835155226345563>")

    @commands.command(aliases=["pickuser", "randommember", "picksomeone"])
    @commands.guild_only()
    async def randomuser(self, ctx):
        """
        Pick a random user in the server.
        """
        await ctx.send(f"<@{random.choice(ctx.guild.members).id}>")

    @commands.command(aliases=["av"])
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, ctx, user: discord.User = None):
        """
        Get a user's avatar.
        """
        if not user:
            user = ctx.author
        png = user.avatar_url_as(format="png", size=4096)
        jpg = user.avatar_url_as(format="jpg", size=4096)
        gif = user.avatar_url_as(static_format="png", size=4096)
        size_512 = user.avatar_url_as(size=512)
        size_1024 = user.avatar_url_as(size=1024)
        size_2048 = user.avatar_url_as(size=2048)
        size_4096 = user.avatar_url_as(size=4096)
        m = (
            f"Formats: [PNG]({png}) | [JPG]({jpg}) | [GIF]({gif})\n"
            f"Sizes: [512]({size_512}) | [1024]({size_1024}) | [2048]({size_2048}) | [4096]({size_4096})"
        )
        embed = discord.Embed(
            color=await ctx.embed_color(),
            title=f"{user.name}'s Avatar:",
            description=m,
        )
        embed.set_image(url=user.avatar_url_as(size=4096))
        await ctx.send(embed=embed)

    @commands.command()
    async def vowelify(self, ctx: commands.Context, *, text: str):
        """
        Multiplies all vowels in a sentence.
        """
        uwuified = "".join(
            [
                c if c in "aeiouAEIOU" else (c * 3 if c not in "aeiou" else c)
                for c in text
            ]
        )
        await ctx.send(uwuified[:1000])

    @commands.command(aliases=["zalgoify"])
    async def zalgo(self, ctx: commands.Context, *, text: str):
        """
        Zalgoifies a sentence.
        """
        t = zalgo.zalgo().zalgofy(text)
        await ctx.send(t[:2000])

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["ship", "lovecalc"])
    async def lovecalculator(self, ctx, user: discord.User, user2: discord.User = None):
        """
        Calculates the amount of love between you and the bot.
        """
        love = random.randint(0, 100)
        if user2 is None:
            user2 = ctx.author
        ua = user.avatar_url_as(static_format="png")
        u2a = user2.avatar_url_as(static_format="png")
        u = f"https://api.martinebot.com/v1/imagesgen/ship?percent={love}&first_user={ua}&second_user={u2a}&no_69_percent_emoji=false"
        t = f"{user.name} and {user2.name} have {love}% compatibility."
        e = discord.Embed(color=await ctx.embed_color(), title=t)
        e.set_image(url=u)
        e.set_footer(text="Powered by api.martinebot.com")
        await ctx.send(embed=e)

    @commands.command(aliases=["peepee", "dingdong"])
    async def pp(self, ctx, *users: discord.Member):
        """
        Get user's peepee size!
        """
        if not users:
            users = (ctx.author,)

        penises = {}
        msg = ""
        state = random.getstate()

        for user in users:
            random.seed(user.id)

            dong_size = random.randint(0, 30)

            penises[user] = "8{}D".format("=" * dong_size)

        random.setstate(state)
        dongs = sorted(penises.items(), key=lambda x: x[1])

        for user, dong in dongs:
            msg += "**{}'s size:**\n{}\n".format(user.display_name, dong)

        for page in pagify(msg):
            await ctx.send(page)

    @commands.is_owner()
    @commands.command()
    async def updr(self, ctx, *cogs: InstalledCog):
        """Update cogs without questioning about reload."""
        ctx.assume_yes = True
        cog_update_command = ctx.bot.get_command("cog update")
        if not cog_update_command:
            await ctx.send(f"I can't find `{ctx.prefix}cog update` command")
            return
        await ctx.invoke(cog_update_command, *cogs)

    @commands.command()
    @commands.is_owner()
    async def unusedrepos(self, ctx):
        """View unused downloader repos."""
        repo_cog = self.bot.get_cog("Downloader")
        if not repo_cog:
            return await ctx.send("Downloader cog not found.")
        repos = [r.name for r in repo_cog._repo_manager.repos]
        active_repos = {c.repo_name for c in await repo_cog.installed_cogs()}
        for r in active_repos:
            try:
                repos.remove(r)
            except:
                pass
        if not repos:
            await ctx.send("All repos are currently being used!")
            return
        await ctx.send(f"Unused: \n" + box(repos, lang="py"))

    # The only thing I made by myself lol.
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def vote(self, ctx):
        """Vote for me!"""
        c = await self.bot.get_embed_colour(await ctx.embed_color())
        t = "Vote for Me!"
        f = "Thanks for your support!"
        i = ctx.bot.user.avatar_url_as(static_format="png")
        
        topgg_link = "https://top.gg/bot/886547720985264178"

        e = discord.Embed(title = t, colour = c)
        e.add_field(name="Links:", value=f"[`Top.gg`]({topgg_link})")
        e.set_thumbnail(url=i)
        e.set_footer(text=f)

        vote_button = [
            ActionRow(
                Button(
                    style=ButtonStyle.link,
                    label="Top.gg",
                    emoji=discord.PartialEmoji(name="topgg", animated=False, id="918280202398875758"),
                    url="https://top.gg/bot/886547720985264178"
                )
            )
        ]
        
        await ctx.send(embed=e, components=vote_button)