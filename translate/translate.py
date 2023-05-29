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

import logging
from typing import Union

import discord
from redbot.core import Config, app_commands, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import humanize_list
from translatepy import Translator
from translatepy.exceptions import TranslatepyException
from translatepy.language import Language
from translatepy.models import TranslationResult
from translatepy.translators import BaseTranslator, YandexTranslate

from .utils import NotFlag, TranslateFlags, deflagize

log = logging.getLogger("red.kuro-cogs.translate")


class Translate(commands.Cog):
    """Translate everything!"""

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.0.1"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=83951226315266)
        self.config.register_guild(react_flag=False)

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.hybrid_command(usage="<text> [flags...]")
    @app_commands.describe(text="The text to translate.")
    async def translate(
        self,
        ctx: commands.Context,
        text: commands.Greedy[NotFlag],
        *,
        flags: TranslateFlags,
    ):
        """
        Translates the given text!

        **Flags**:
        - `--from`: The language to translate from. Auto-detect if not provided.
        - `--to`: The language to translate to. Defaults to English if not provided.
        - `--translator`: The translator to use. Automatically chosen if not provided.

        Translators:
        - `bing`: Bing
        - `deepl`: DeepL
        - `google`: Google
        - `libre`: Libre
        - `mymemory`: MyMemory
        - `reverso`: Reverso
        - `translatecom`: Translate.com
        - `yandex`: Yandex

        **Examples**:
        - `[p]translate Ejemplo de texto --to English` (Translates "Ejemplo de texto" to English)
        - `[p]translate Example of text --from English --to Español` (Translates "Example of Text" from English to Español)
        """
        if not text:
            await ctx.send_help()
            return
        text = " ".join(text)
        try:
            result = await self._translate(
                text, flags.translator, str(flags.to_lang), str(flags.from_lang)
            )
        except TranslatepyException as error:
            await ctx.send(f"{error}.")
        else:
            await self.send_translation_result(ctx, result, ctx.author)

    @commands.command(aliases=["tte"])
    async def texttoemoji(self, ctx: commands.Context, *, text: str):
        """Convert the given text to emojis!"""
        try:
            result = await self._translate(text, YandexTranslate(), "emj")
        except TranslatepyException as error:
            await ctx.send(f"{error}.")
            return

        if not await ctx.embed_requested():
            await ctx.send(f"{result}\n\nRequested by: {ctx.author}")
            return
        embed = discord.Embed(description=str(result), color=await ctx.embed_color())
        embed.set_footer(text=f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, user: Union[discord.Member, discord.User]
    ):
        if user.bot:
            return
        message = reaction.message
        if await self.bot.cog_disabled_in_guild(self, message.guild):
            return
        ctx = await self.bot.get_context(message)
        if await self.bot.ignored_channel_or_guild(ctx):
            return
        if not message.content:
            return
        if not isinstance(reaction.emoji, str):
            return
        deflagized, success = deflagize(reaction.emoji)
        if not success:
            return
        try:
            language = Language(deflagized, threshold=63)
            result = await self._translate(message.content, Translator(), str(language))
        except TranslatepyException as exc_info:
            log.exception(
                f"Error while translating message (ID: {message.id}) with reaction.",
                exc_info=exc_info,
            )
        else:
            await self.send_translation_result(ctx, result, user)

    async def _translate(
        self,
        text: str,
        translator: Union[BaseTranslator, Translator],
        to_language: str,
        from_language: str = "auto",
    ) -> TranslationResult:
        result = await self.bot.loop.run_in_executor(
            None, translator.translate, text, to_language, from_language
        )
        return result

    @staticmethod
    async def send_translation_result(
        ctx: commands.Context,
        result: TranslationResult,
        author: Union[discord.Member, discord.User],
    ):
        footer = (
            f"{result.source_language.name} to {result.destination_language.name} | "
            f"Translated with {result.service}\nRequested by: {author}"
        )
        if not await ctx.embed_requested():
            await ctx.send(f"{result}\n\n{footer}")
            return
        embed = discord.Embed(description=str(result), color=await ctx.embed_color())
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)
