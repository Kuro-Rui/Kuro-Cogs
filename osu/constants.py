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

import re

from aiosu.models import Gamemode

GAME_MODES = [Gamemode.STANDARD, Gamemode.TAIKO, Gamemode.CTB, Gamemode.MANIA]

USER_LINK_REGEX = re.compile(r"https://osu\.ppy\.sh/u(?:sers)?/(?P<user_id>\d+)")

BEATMAP_LINK_REGEX = re.compile(r"https://osu\.ppy\.sh/b(?:eatmaps)?/(?P<beatmap_id>\d+)")

BEATMAPSET_LINK_REGEX = re.compile(
    r"https://osu\.ppy\.sh/beatmapsets/(?P<beatmapset_id>\d+)#?(?P<gamemode>osu|taiko|fruits|mania)?/?(?P<beatmap_id>\d+)?"
)

RANK_EMOJIS = {
    "ssh": 1102049862624747631,
    "ss": 1102049896720236556,
    "sh": 1102049938319355924,
    "s": 1102049963707486208,
    "a": 1102049988873293915,
}

MODE_EMOJIS = {
    "std": 1205565233158951005,
    "taiko": 1205565318739796008,
    "ctb": 1205565349227929670,
    "mania": 1205565371394822185,
}

DIFFICULTY_EMOJIS = {
    "std": {
        "easy": 1205547438211862560,
        "normal": 1205547537839423590,
        "hard": 1205547626527727736,
        "insane": 1205555171057205349,
        "expert": 1205560511857696768,
        "expert+": 1205560866481643530,
        "extreme": 1205561020261601380,
        "black": 1205561135038861372,
    },
    "taiko": {
        "easy": 1205547465911181324,
        "normal": 1205547560106725427,
        "hard": 1205547649714094090,
        "insane": 1205555171162067056,
        "expert": 1205560536477995038,
        "expert+": 1205560890296897677,
        "extreme": 1205561055447883859,
        "black": 1205561181180530748,
    },
    "ctb": {
        "easy": 1205547489302810634,
        "normal": 1205547582600781894,
        "hard": 1205547675240505354,
        "insane": 1205560454080888853,
        "expert": 1205560567298007140,
        "expert+": 1205560912514129981,
        "extreme": 1205561081557155902,
        "black": 1205561206388031488,
    },
    "mania": {
        "easy": 1205547513315069954,
        "normal": 1205547604692439122,
        "hard": 1205547697969434704,
        "insane": 1205560476201779271,
        "expert": 1205560589158715423,
        "expert+": 1205560967484809287,
        "extreme": 1205561102797111326,
        "black": 1205561230148898886,
    },
}

STATUS_IMAGES = {
    "graveyard": "https://cdn.discordapp.com/emojis/1205546835721064548.png?quality=lossless",
    "wip": "https://cdn.discordapp.com/emojis/1205546835721064548.png?quality=lossless",
    "pending": "https://cdn.discordapp.com/emojis/1205546835721064548.png?quality=lossless",
    "ranked": "https://cdn.discordapp.com/emojis/1205546879757328385.png?quality=lossless",
    "approved": "https://cdn.discordapp.com/emojis/1205546858630615151.png?quality=lossless",
    "qualified": "https://cdn.discordapp.com/emojis/1205546858630615151.png?quality=lossless",
    "loved": "https://cdn.discordapp.com/emojis/1205546897738047508.png?quality=lossless",
}
