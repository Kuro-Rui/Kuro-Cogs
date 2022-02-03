import aiohttp

import discord

from redbot.core import Config, commands

import urllib
from zalgo_text import zalgo

# from .ssc_phrases import SORBET_SHARK_COOKIE_PHRASES

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

    # @commands.command(aliases=["sorbetshark"])
    # async def sorbetsharkcookie(self, ctx: commands.Context, *, text: str):
        # """
        # Turns a text into Sorbet Shark Cookie's language.
        # """
        # lower_text = text.lower()

        # # Need to space each word so It doesn't get confusing :D
        # text.replace("a", "OoO ")
        # text.replace("b", "ooO ")
        # text.replace("c", "Ooo ")
        # text.replace("d", "O-o ")
        # text.replace("e", "OU ")
        # text.replace("f", "OOo ")
        # text.replace("g", "oOo ")
        # text.replace("h", "O-O ")
        # text.replace("i", "o-o-o ")
        # text.replace("j", "O--O ")
        # text.replace("k", "oOuú ")
        # text.replace("l", "OoŒ ")
        # text.replace("m", "oÖ ")
        # text.replace("n", "OuUo ")
        # text.replace("o", "uuooOo ")
        # text.replace("p", "UuoOo ")
        # text.replace("q", "UuoOo ")
        # text.replace("r", "OuUuO ")
        # text.replace("s", "oOuuU ")
        # text.replace("t", "UuOo ")
        # text.replace("u", "UuOo ")
        # text.replace("v", "oouuuo ")
        # text.replace("w", "OuOo ")
        # text.replace("x", "OooOuu ")
        # text.replace("y", "uuooouu ")
        # text.replace("z", "ouuuouuu ")

        # await ctx.send(text.replace(f"{lower_text}", SORBET_SHARK_COOKIE_PHRASES))
