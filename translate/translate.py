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
from translatepy import Translator
from translatepy.translators import *

from .utils import LanguageConverter, send_result


class Translate(commands.Cog):
    """Translate everything!"""

    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.deepl = DeeplTranslate()
        self.google = GoogleTranslate()
        self.libre = LibreTranslate()
        self.mymemory = MyMemoryTranslate()
        self.reverso = ReversoTranslate()
        self.translatecom = TranslateComTranslate()
        self.yandex = YandexTranslate()

    __author__ = humanize_list(["Kuro"])
    __version__ = "2.1.0"

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
        to_language: LanguageConverter,
        from_language: Optional[LanguageConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]translate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]translate es en Example of text` (Translates "Example of Text" from English to Español)
        """

        await send_result(self, ctx, text, from_language, to_language, "Auto")

    @commands.command(aliases=["dltranslate", "deepltranslate"])
    async def dtranslate(
        self,
        ctx,
        to_language: LanguageConverter,
        from_language: Optional[LanguageConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text with DeepL!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]dtranslate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]dtranslate es en Example of text` (Translates "Example of Text" from English to Español)
        """

        await send_result(self, ctx, text, from_language, to_language, "DeepL")

    @commands.command(aliases=["googletranslate"])
    async def gtranslate(
        self,
        ctx,
        to_language: LanguageConverter,
        from_language: Optional[LanguageConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text with Google Translate!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]gtranslate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]gtranslate es en Example of text` (Translates "Example of Text" from English to Español)
        """

        await send_result(self, ctx, text, from_language, to_language, "Google")

    @commands.command(aliases=["libretranslate"])
    async def ltranslate(
        self,
        ctx,
        to_language: LanguageConverter,
        from_language: Optional[LanguageConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text with LibreTranslate!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]ltranslate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]ltranslate es en Example of text` (Translates "Example of Text" from English to Español)
        """

        await send_result(self, ctx, text, from_language, to_language, "Libre")

    @commands.command(aliases=["mymemtranslate", "mymemorytranslate"])
    async def mmtranslate(
        self,
        ctx,
        to_language: LanguageConverter,
        from_language: Optional[LanguageConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text with MyMemory!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]mmtranslate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]mmtranslate es en Example of text` (Translates "Example of Text" from English to Español)
        """

        await send_result(self, ctx, text, from_language, to_language, "MyMemory")

    @commands.command(aliases=["reversotranslate"])
    async def rtranslate(
        self,
        ctx,
        to_language: LanguageConverter,
        from_language: Optional[LanguageConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text with Reverso!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]rtranslate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]rtranslate es en Example of text` (Translates "Example of Text" from English to Español)
        """

        await send_result(self, ctx, text, from_language, to_language, "Reverso")

    @commands.command(aliases=["ttranslate", "translatecom"])
    async def tctranslate(
        self,
        ctx,
        to_language: LanguageConverter,
        from_language: Optional[LanguageConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text with Translate.com!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]tctranslate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]tctranslate es en Example of text` (Translates "Example of Text" from English to Español)
        """

        await send_result(self, ctx, text, from_language, to_language, "Translate.com")

    @commands.command(aliases=["yandextranslate"])
    async def ytranslate(
        self,
        ctx,
        to_language: LanguageConverter,
        from_language: Optional[LanguageConverter] = "Auto",
        *,
        text: str,
    ):
        """
        Translates the given text with Yandex Translate!

        You can also provide a language to translate from (`from_language`).
        **Examples**:
            - `[p]ytranslate en Ejemplo de texto` (Translates "Ejemplo de texto" to English)
            - `[p]ytranslate es en Example of text` (Translates "Example of Text" from English to Español)
        """

        await send_result(self, ctx, text, from_language, to_language, "Yandex")

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
