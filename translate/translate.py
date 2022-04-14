from translatepy import Language, Translator
from translatepy.exceptions import TranslatepyException, UnknownLanguage

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list


class Translate(commands.Cog):
    """Translate everything!"""

    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.command()
    async def translate(self, ctx, from_language: str, to_language: str, *, text: str):
        """
        Translates the given text!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]translate en es Example Text` (Translates "Example Text" to Español)
            - `[p]translate es en Ejemplo de texto` (Translates "Ejemplo de texto" from Español to English)
        """

        from_language = await self.language_converter(ctx, from_language)
        to_language = await self.language_converter(ctx, to_language)

        try:
            result = self.translator.translate(text, to_language, from_language)
        except TranslatepyException:
            return await ctx.send("An error occurred while translating. Please try again later.")

        footer = f"{from_language} to {to_language} | Translated with {result.service}."
        if await ctx.embed_requested():
            embed = discord.Embed(description=result, color=await ctx.embed_color())
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{result}\n\n{footer}")

    async def language_converter(self, ctx, language: str):
        try:
            return Language(language).alpha2.upper()
        except UnknownLanguage as ul:
            await ctx.send(
                f"I can't find the language `{language}`. Do you mean `{ul.guessed_language}`?"
            )
            return

    @commands.command(aliases=["tte"])
    async def texttoemoji(self, ctx, *, text: str):
        """Convert the given text to emojis!"""

        result = self.translator.translate(text, "EMJ")
        footer = f"Requested by {ctx.author}"
        if await ctx.embed_requested():
            embed = discord.Embed(description=result, color=await ctx.embed_color())
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{result}\n\n{footer}")
