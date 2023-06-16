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
from urllib.parse import parse_qs, urlparse

from aiosu.models import Gamemode
from redbot.core.utils.chat_formatting import humanize_number


def maybe_humanize_number(number: Optional[int], alt: str) -> str:
    if number:
        return humanize_number(number)
    return alt


def parse_code_from_url(url: str) -> str:
    query = urlparse(url).query
    code = parse_qs(query).get("code")
    if code is None:
        raise KeyError(f"Passed URL contains does not have 'code' parameter.")
    if len(code) > 1:
        raise ValueError(f"Passed URL contains multiple values for 'code' parameter.")
    return code[0]


DEFAULT_MODE_EMOJIS = {
    "std": 1102048785481338990,
    "taiko": 1102048811595079680,
    "ctb": 1102048833875222528,
    "mania": 1102048854708330570,
}

DEFAULT_RANK_EMOJIS = {
    "ssh": 1102049862624747631,
    "ss": 1102049896720236556,
    "sh": 1102049938319355924,
    "s": 1102049963707486208,
    "a": 1102049988873293915,
}

GAME_MODES = [Gamemode.STANDARD, Gamemode.TAIKO, Gamemode.CTB, Gamemode.MANIA]
