"""
MIT License

Copyright (c) 2021-present Kuro-Rui

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Optional

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list
from translatepy import Language, Translator
from translatepy.exceptions import TranslatepyException, UnknownLanguage


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

    # Thanks Fixator! You helped me in almost everything lol.
    @commands.command()
    async def translate(
        self,
        ctx,
        to_language: LangConverter,
        from_language: Optional[LangConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]translate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]translate es en Example Text` (Translates "Example Text" from English to Español)
        """

        try:
            result = await self.bot.loop.run_in_executor(
                None, self.translator.translate, text, to_language, from_language
            )
        except TranslatepyException as error:
            return await ctx.send(error)

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
