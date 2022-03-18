import aiohttp
from io import BytesIO
import random
from random import choice

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list

from .fumo import FUMO


class Fumo(commands.Cog):
    """
    Basically Fumos.
    Kuro is ~~not~~ a Fumo Simp.
    """

    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.1.2"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )
    
    @commands.group()
    async def fumo(self, ctx):
        """Generates Fumo Image."""
        pass

    @fumo.command(aliases=["images", "random"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def image(self, ctx):
        """Generates a random Fumo image."""
        e = discord.Embed(title="Here's a Random Fumo Image! 🎏", color=await ctx.embed_color())
        e.set_image(url=choice(FUMO["list"]))
        e.set_footer(text="Source: Kuro-Cogs/blob/main/fumo/fumo.py", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
        await ctx.send(embed=e)

    @fumo.command(aliases=["gifs"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def gif(self, ctx):
        """Generates a random Fumo GIF."""
        e = discord.Embed(title="Here's a Random Fumo GIF! 🎏", color=await ctx.embed_color())
        e.set_image(url=choice(FUMO["gifs"]))
        e.set_footer(text="Source: Kuro-Cogs/blob/main/fumo/fumo.py", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
        await ctx.send(embed=e)

    @fumo.command(aliases=["memes"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meme(self, ctx):
        """Generates a random Fumo meme."""
        e = discord.Embed(title="Here's a Random Fumo Meme! 🎏", color=await ctx.embed_color())
        e.set_image(url=choice(FUMO["memes"]))
        e.set_footer(text="Source: Kuro-Cogs/blob/main/fumo/fumo.py", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Fumo(bot))

__red_end_user_data_statement__ = "This cog does not store any end user data."