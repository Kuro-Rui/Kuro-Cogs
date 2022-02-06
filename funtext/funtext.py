import aiohttp

import discord

from redbot.core import Config, commands

import urllib
from zalgo_text import zalgo

# I stole this from https://github.com/kaogurai/cogs/blob/master/kaotools/kaotools.py#L445-L476
class FunText(commands.Cog):
    """
    Generate a fun text from your given text :D
    """

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(aliases=["uwuify", "owo", "owoify"])
    async def uwu(self, ctx: commands.Context, *, text: str):
        """
        Uwuifies a sentence.
        """
        encoded = urllib.parse.quote(text)
        async with self.session.get(
            f"https://owo.l7y.workers.dev/?text={encoded}"
        ) as req:
            if req.status == 200:
                data = await req.text()
                await ctx.send(data[:1000])
            else:
                await ctx.send("S-S-Sowwy, s-sometwhing went w-wwong... (°ロ°)")
    
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

    @commands.command(aliases=["sorbetshark"])
    async def sorbetsharkcookie(self, ctx: commands.Context, *, text: str):
        """
        Turns a text into Sorbet Shark Cookie's language.
        """
        # ⚠️WARNING⚠️: Way too unefficient 😃
        text = text.lower()
        replaced_text = text.replace("a", "OoO ")
        replaced_text = text.replace("b", "ooO ")
        replaced_text = text.replace("c", "Ooo ")
        replaced_text = text.replace("d", "O-o ")
        replaced_text = text.replace("e", "OU ")
        replaced_text = text.replace("f", "OOo ")
        replaced_text = text.replace("g", "oOo ")
        replaced_text = text.replace("h", "O-O ")
        replaced_text = text.replace("i", "o-o-o ")
        replaced_text = text.replace("j", "O--O ")
        replaced_text = text.replace("k", "oOuú ")
        replaced_text = text.replace("l", "OoŒ ")
        replaced_text = text.replace("m", "oÖ ")
        replaced_text = text.replace("n", "OuUo ")
        replaced_text = text.replace("o", "uuooOo ")
        replaced_text = text.replace("p", "UuoOo ")
        replaced_text = text.replace("q", "UuoOo ")
        replaced_text = text.replace("r", "OuUuO ")
        replaced_text = text.replace("s", "oOuuU ")
        replaced_text = text.replace("t", "UuOo ")
        replaced_text = text.replace("u", "UuOo ")
        replaced_text = text.replace("v", "oouuuo ")
        replaced_text = text.replace("w", "OuOo ")
        replaced_text = text.replace("x", "OooOuu ")
        replaced_text = text.replace("y", "uuooouu ")
        replaced_text = text.replace("z", "ouuuouuu ")

        await ctx.send(replaced_text)
