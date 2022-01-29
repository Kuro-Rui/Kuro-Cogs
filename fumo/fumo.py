import aiohttp

import discord
from redbot.core import commands

from .fumos import FUMO


class Fumo(commands.Cog):
    """
    Basically Fumos.
    
    Kuro is ~~not~~ a Fumo Simp.
    """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fumo(self, ctx):
        """Generates Fumo Image."""
        pass

    @fumo.commands()
    async def random(self, ctx):
        """Generates a random Fumo image."""
        async with ctx.typing():
            e = discord.Embed(title="Here's a Random Fumo Image! 🎏", color=await ctx.embed_color())
            e.set_image(url=FUMO["list"])
            e.set_footer(text="Source: github.com/Kuro-Rui/Kuro-Cogs/blob/main/fumo/fumos.py", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
            await ctx.send(embed=e)

    @fumo.commands(aliases=["gifs"])
    async def gif(self, ctx):
        """Generates a random Fumo GIF."""
        async with ctx.typing():
            e = discord.Embed(title="Here's a Random Fumo GIF! 🎏", color=await ctx.embed_color())
            e.set_image(url=FUMO["gifs"])
            e.set_footer(text="Source: github.com/Kuro-Rui/Kuro-Cogs/blob/main/fumo/fumos.py", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
            await ctx.send(embed=e)

    @fumo.commands(aliases=["memes"])
    async def meme(self, ctx):
        """Generates a random Fumo meme."""
        async with ctx.typing():
            e = discord.Embed(title="Here's a Random Fumo Meme! 🎏", color=await ctx.embed_color())
            e.set_image(url=FUMO["memes"])
            e.set_footer(text="Source: github.com/Kuro-Rui/Kuro-Cogs/blob/main/fumo/fumos.py", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
            await ctx.send(embed=e)

    @fumo.commands(aliases=["videos"])
    async def video(self, ctx):
        """Generates a random Fumo video."""
        async with ctx.typing():
            e = discord.Embed(title="Here's a Random Fumo Image! 🎏", color=await ctx.embed_color())
            f = discord.File(FUMO["videos"], filename="fumo.mp4")
            e.set_image(url="attachment://fumo.mp4")
            e.set_footer(text="Source: github.com/Kuro-Rui/Kuro-Cogs/blob/main/fumo/images.py", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
            await ctx.send(embed=e, file=f)
            f.close()