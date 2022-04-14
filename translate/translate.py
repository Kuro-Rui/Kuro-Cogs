from translatepy import Language, Translator
from translatepy.exceptions import TranslatepyException, UnknownLanguage
from typing import Optional

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list


class LangConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            lang = Language(argument)
            if lang.similarity < 100:
                raise commands.BadArgument()
            return lang
        except UnknownLanguage as ul:
            raise commands.BadArgument(
                f"Unable to find `{argument}`. Did you mean `{ul.guessed_language}`?"
            )


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
    async def translate(
        self,
        ctx,
        from_language: Optional[LangConverter],
        to_language: LangConverter,
        *,
        text: str
    ):
        """
        Translates the given text!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]translate en es Example Text` (Translates "Example Text" to Español)
            - `[p]translate en Ejemplo de texto` (Translates "Ejemplo de texto" from Español to English)
        """

        if not from_language:
            from_language = "Auto"
        try:
            result = await self.bot.loop.run_in_executor(
                None,
                self.translator.translate,
                text,
                to_language,
                from_language
            )
        except TranslatepyException:
            return await ctx.send("An error occurred while translating. Please try again later.")

        footer = (
            f"{result.source_language.name} to {result.destination_language.name} | "
            f"Translated with {result.service}\nRequested by: {ctx.author}"
        )
        if await ctx.embed_requested():
            embed = discord.Embed(description=result, color=await ctx.embed_color())
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{result}\n\n{footer}")

    @commands.command(aliases=["tte"])
    async def texttoemoji(self, ctx, *, text: str):
        """Convert the given text to emojis!"""

        result = self.translator.translate(text, "EMJ")
        footer = f"Requested by: {ctx.author}"
        if await ctx.embed_requested():
            embed = discord.Embed(description=result, color=await ctx.embed_color())
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{result}\n\n{footer}")
