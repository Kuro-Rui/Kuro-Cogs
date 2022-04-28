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
from translatepy import Language
from translatepy.exceptions import TranslatepyException, UnknownLanguage


class LanguageConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            lang = Language(argument)
            if lang.similarity < 100:
                raise commands.BadArgument(f"Unable to find `{argument}`.")
            return lang
        except UnknownLanguage as ul:
            raise commands.BadArgument(
                f"Unable to find `{argument}`. Did you mean `{ul.guessed_language}`?"
            )


async def send_result(
    self,
    ctx,
    text: str,
    from_language: LanguageConverter,
    to_language: LanguageConverter,
    translator: str,
):
    """Sends Translate Result"""

    # Don't mind the long-ass ifs lol :v
    if translator == "Auto":
        translator = self.translator
    elif translator == "DeepL":
        translator = self.deepl
    elif translator == "Google":
        translator = self.google
    elif translator == "Libre":
        translator = self.libre
    elif translator == "MyMemory":
        translator = self.mymemory
    elif translator == "Reverso":
        translator = self.reverso
    elif translator == "Translate.com":
        translator = self.translatecom
    elif translator == "Yandex":
        translator = self.yandex

    try:
        result = await self.bot.loop.run_in_executor(
            None, translator.translate, text, to_language, from_language
        )
    except TranslatepyException as error:
        return await ctx.send(f"{error}.")

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
