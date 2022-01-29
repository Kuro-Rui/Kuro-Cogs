import aiohttp
from io import BytesIO
import random
from random import choice

import discord
from redbot.core import commands

from .fumo import FUMO


class Fumo(commands.Cog):
    """
    Basically Fumos.
    Kuro is ~~not~~ a Fumo Simp.
    """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def fumo(self, ctx):
        """Generates Fumo Image."""
        pass

    @fumo.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def random(self, ctx):
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

    @fumo.command(aliases=["videos"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def video(self, ctx):
        """Generates a random Fumo video."""
        async with ctx.typing():
            c = "**Here's a Random Fumo Video!** 🎏"
            e = discord.Embed(title=c, color=await ctx.embed_color())
            f = discord.File(BytesIO(choice(FUMO["videos"])), filename="fumo.mp4")
            e.set_image(url="attachment://fumo.mp4")
            e.set_footer(text="Source: Kuro-Cogs/blob/main/fumo/fumo.py", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
            await ctx.send(embed=e, file=f)
            f.close()

def setup(bot):
    bot.add_cog(Fumo(bot))

__red_end_user_data_statement__ = "This cog does not store any end user data."