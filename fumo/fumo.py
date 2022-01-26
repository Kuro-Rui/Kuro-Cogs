import aiohttp

import discord

from redbot.core import commands


class Fumo(commands.Cog):
    """Basically Fumos.
    
    Kuro is ~~not~~ a Fumo Simp.
    """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fumo(self, ctx):
        """Generates a random Fumo image."""
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get(f"https://fumoapi.herokuapp.com/random") as r:
                    fumo = await r.json()
                    # Embed Thingy :D
                    e = discord.Embed(title="Here's a Fumo Image! 🎏", color=await ctx.embed_color())
                    e.set_image(url=fumo["URL"])
                    e.set_footer(text="Powered by fumoapi.herokuapp.com", icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless")
                    await ctx.send(embed=e)
