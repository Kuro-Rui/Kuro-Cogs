from random import choice
import discord

from .fumos import fumo

async def gensokyo_status(self) -> bool:
    """Fumo API Status"""
    async with self.session.get("https://fumoapi.herokuapp.com/random") as response:
        if response.status == 200:
            return True
        else:
            return False

async def fumo_calling_ritual(self):
    """Fumo API Call."""
    if await gensokyo_status(self):
        async with self.session.get("https://fumoapi.herokuapp.com/random") as response:
            get_fumo = await response.json()
            return get_fumo["URL"]
    else:
        return

async def summon_fumo(self, ctx, type: str):
    """Summon a Fumo."""
    e = discord.Embed(color=await ctx.embed_color())
    if type == "random":
        get_fumo = await fumo_calling_ritual(self)
        if fumo:
            e.title = f"Here's a Random Fumo! 🎏"
            e.set_image(url=get_fumo)
            e.set_footer(
                text="Source: https://fumoapi.herokuapp.com/",
                icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless"
            )
        else:
            return await ctx.send("There's something wrong with the Fumo API, try again later!")
    else:
        e.title = f"Here's a Random Fumo {type.title()}! 🎏"
        e.set_image(url=choice(fumo[type]))
        e.set_footer(
            text="Source: Kuro-Cogs/blob/main/fumo/fumos.py",
            icon_url="https://cdn.discordapp.com/emojis/935839733173612594.gif?size=128&quality=lossless"
        )
    await ctx.send(embed=e)