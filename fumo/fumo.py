import aiohttp

import discord

from redbot.core import commands


class Fumo(commands.Cog):
    """Basically Fumos."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def fumo(self, ctx):
        """Generates a random Fumo image."""
        async with aiohttp.ClientSession() as s:
                async with s.get(f"https://fumoapi.herokuapp.com/random") as r:
                    fumo = await r.json()

                    e = discord.Embed(title="Here's a Fumo Image!", color=await ctx.embed_color())
                    e.set_image(url=fumo["URL"])
                    await ctx.send(embed=e)
