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

from emoji import UNICODE_EMOJI_ENGLISH
from redbot.core.commands import BadArgument, Context, Converter, EmojiConverter

from .utils import NoExitParser


class Emoji(EmojiConverter):
    async def convert(self, ctx: Context, argument: str):
        if argument in UNICODE_EMOJI_ENGLISH:
            return argument
        return str(await super().convert(ctx, argument))


# Thanks Flare (https://github.com/flaree/flare-cogs/blob/master/giveaways/converter.py#L15-L212)
class Args(Converter):
    async def convert(self, ctx: Context, argument: str) -> dict:
        argument = argument.replace("—", "--")  # For iOS's weird smart punctuation

        parser = NoExitParser(add_help=False)
        parser.add_argument("username", nargs="*", default=None, type=str)
        parser.add_argument("--mode", nargs="?", default="standard", type=str)

        try:
            values = vars(parser.parse_args(argument.split(" ")))
        except Exception:
            raise BadArgument()

        username = await ctx.bot.get_cog("Osu").config.user(ctx.author).username()
        if not values["username"]:
            if username:
                values["username"] = username
            else:
                values["username"] = None
        if values["username"]:
            values["username"] = " ".join(values["username"])

        modes = ["std", "standard", "taiko", "ctb", "catch", "catchthebeat", "mania"]
        if values["mode"] not in modes:
            raise BadArgument()
        if values["mode"] in ["std", "standard"]:
            values["mode"] = 0
        elif values["mode"] == "taiko":
            values["mode"] = 1
        elif values["mode"] in ["ctb", "catch", "catchthebeat"]:
            values["mode"] = 2
        elif values["mode"] == "mania":
            values["mode"] = 3

        return values
