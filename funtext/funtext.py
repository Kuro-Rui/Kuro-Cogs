import aiohttp

import discord

from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list

import urllib
from zalgo_text import zalgo

# I stole this from https://github.com/kaogurai/cogs/blob/master/kaotools/kaotools.py#L445-L476
class FunText(commands.Cog):
    """
    Generate a fun text from your given text :D
    """

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    __author__ = humanize_list(["alec", "Kuro"])
    __version__ = "1.0.1"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Authors :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.command(aliases=["uwuify", "owo", "owoify"])
    async def uwu(self, ctx: commands.Context, *, text: str):
        """
        Uwuifies a sentence.
        """
        encoded = urllib.parse.quote(text)
        async with self.session.get(f"https://owo.l7y.workers.dev/?text={encoded}") as req:
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
            [c if c in "aeiouAEIOU" else (c * 3 if c not in "aeiou" else c) for c in text]
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
        # O and U first
        text = text.replace("o", "ooOo ")
        text = text.replace("u", "uUuu ")
        # Then whatever
        text = text.replace("a", "OoO ")
        text = text.replace("b", "ooO ")
        text = text.replace("c", "Ooo ")
        text = text.replace("d", "O-o ")
        text = text.replace("e", "OU ")
        text = text.replace("f", "OOo ")
        text = text.replace("g", "oOo ")
        text = text.replace("h", "O-O ")
        text = text.replace("i", "o-o-o ")
        text = text.replace("j", "O--O ")
        text = text.replace("k", "oOuú ")
        text = text.replace("l", "OoŒ ")
        text = text.replace("m", "oÖ ")
        text = text.replace("n", "OuUo ")
        text = text.replace("p", "UuoOo ")
        text = text.replace("q", "UuoOo ")
        text = text.replace("r", "OuUuO ")
        text = text.replace("s", "oOuuU ")
        text = text.replace("t", "UuOo ")
        text = text.replace("v", "oouuuo ")
        text = text.replace("w", "OuOo ")
        text = text.replace("x", "OooOuu ")
        text = text.replace("y", "uuooouu ")
        text = text.replace("z", "ouuuouuu ")

        await ctx.send(text)
