import random
from random import choice

import discord

import redbot
from redbot.core import commands

from .images import foods, food_emojis

class CursedImages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cursedfoods"])
    async def cursedfood(self, ctx):
        """Generates a random cursed food image."""
        t = "Here's Cursed Food Image... {}".format(random.choice(food_emojis))
        d = "⚠️**TW⚠️ : CURSED FOOD IMAGES**"
        e = discord.Embed(title=t, description=d, color=await ctx.embed_color())
        e.set_image(url=random.choice(foods))
        await ctx.send(embed=e)