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

try:
    from emoji import UNICODE_EMOJI_ENGLISH as EMOJI_DATA  # emoji<2.0.0
except ImportError:
    from emoji import EMOJI_DATA  # emoji>=2.0.0
from redbot.core import commands

log = logging.getLogger("red.kuro-cogs.osu")


class Emoji(commands.EmojiConverter):
    async def convert(self, ctx: commands.Context, argument: str) -> Union[str, int]:
        if argument in EMOJI_DATA:
            return argument
        emoji = await super().convert(ctx, argument)
        return emoji.id


class Mode(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> str:
        if argument.lower() in ("std", "standard", "osu"):
            return "STD"
        if argument.lower() == "taiko":
            return "Taiko"
        if argument.lower() in ("ctb", "catch", "fruits"):
            return "CTB"
        if argument.lower() == "mania":
            return "Mania"
        raise commands.BadArgument(
            "Invalid mode type. Valid modes are either `std`, `taiko`, `ctb`, or `mania`."
        )


class QueryType(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> str:
        if argument.lower() in ("string", "username"):
            return "string"
        if argument.lower() in ("id", "userid"):
            return "id"
        raise commands.BadArgument(
            "Invalid query type. Valid types are either `username` or `userid`."
        )


class Rank(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> str:
        if argument.lower() in ("ssh", "ss", "sh", "s", "a"):
            return argument.lower()
        raise commands.BadArgument(
            "Invalid rank type. Valid ranks are either `ssh`, `ss`, `sh`, `s`, or `a`."
        )
