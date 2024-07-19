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

from typing import Literal, Optional
from urllib.parse import parse_qs, urlparse

from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import humanize_number

from .constants import DIFFICULTY_EMOJIS, MODE_EMOJIS


def maybe_humanize_number(number: Optional[int], alt: str) -> str:
    return humanize_number(number) if number else alt


def maybe_get_emoji(bot: Red, emoji_id: int, alt: str) -> Optional[str]:
    emoji = bot.get_emoji(emoji_id)
    return str(emoji) if emoji else alt


def get_difficulty_emoji(mode: Literal["std", "taiko", "ctb", "mania"], star_rating: float) -> str:
    emojis = DIFFICULTY_EMOJIS[mode]
    # https://osu.ppy.sh/wiki/en/Beatmap/Difficulty#difficulty-and-star-rating
    if star_rating < 2:
        return str(emojis["easy"])
    elif star_rating < 2.7:
        return str(emojis["normal"])
    elif star_rating < 4:
        return str(emojis["hard"])
    elif star_rating < 5.3:
        return str(emojis["insane"])
    elif star_rating < 6.5:
        return str(emojis["expert"])
    elif star_rating < 8:
        return str(emojis["expert+"])
    elif star_rating < 9:
        return str(emojis["extreme"])
    elif star_rating >= 9:
        return str(emojis["black"])
    else:
        return str(MODE_EMOJIS[mode])


def parse_code_from_url(url: str) -> str:
    query = urlparse(url).query
    code = parse_qs(query).get("code")
    if code is None:
        raise KeyError(f"Passed URL contains does not have 'code' parameter.")
    if len(code) > 1:
        raise ValueError(f"Passed URL contains multiple values for 'code' parameter.")
    return code[0]
