from io import BytesIO
from random import choice

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list

from .images import food_emojis, food_images


class CursedImages(commands.Cog):
    """Just a cringe cog that returns cursed images."""

    def __init__(self, bot):
        self.bot = bot

    __author__ = "Kuro"
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.command(aliases=["cursedfoods"])
    async def cursedfood(self, ctx):
        """Generates a random cursed food image."""
        t = "Here's Cursed Food Image... {}".format(choice(food_emojis))
        d = "⚠️**TW⚠️ : CURSED FOOD IMAGES**"
        e = discord.Embed(title=t, description=d, color=await ctx.embed_color())
        e.set_image(url=choice(food_images))
        await ctx.send(embed=e)
