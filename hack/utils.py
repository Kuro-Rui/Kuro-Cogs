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

from random import choice, shuffle
from re import UNICODE, compile
from string import ascii_letters, digits, punctuation

import discord


def loading(step: int):
    steps = ["▖", "▘", "▝", "▗"]
    screen = f"[{steps[step]}]"
    return screen


def remove_emoji(text: str):
    compiled = compile(
        (
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
            "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
            "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
            "]+"
        ),
        UNICODE,
    )
    return compiled.sub(r"", text)


def remove_punctuations(text: str):
    letters = list(text)
    for letter in letters:
        if letter in punctuation:
            letters.remove(letter)
    text = "".join(letters)
    return text


def get_email_and_password(user: discord.Member):
    name = remove_emoji(remove_punctuations(user.name.lower()))
    name = name.replace(" ", "").replace("'", "").replace('"', "")
    domain = choice(
        [
            "@aol.com",
            "@disposablemail.com",
            "@edu.com",
            "@gmail.com",
            "@gmx.net",
            "@hotmail.com",
            "@icloud.com",
            "@msn.com",
            "@outlook.com",
            "@protonmail.com",
            "@yahoo.com",
            "@yandex.com",
        ]
    )
    email = name + domain
    letters = "".join(choice(ascii_letters) for letters in range(6))
    numbers = "".join(choice(digits) for numbers in range(5))
    puncts = "".join(choice(punctuation) for puncts in range(4))
    password = list(letters + numbers + puncts)
    shuffle(password)
    password = "".join(password).replace("`", "'")
    return email, password


def get_last_dm():
    last_dm = choice(
        [
            "I hope blueballs aren't real.",
            "I hope noone sees my nudes folder.",
            "I think it's smaller than most.",
            "UwU",
            "can I see your feet pics?",
            "dont frgt to like and subscrube!!",
            "honestly I'm pretty sure blue waffle is real and I have it.",
            "imagine having a peen as small as mine in 2022",
            "man I love my mommy.",
            "pwetty pwease?",
            "yeah I'm just built different.",
            "yeah she goes to another school.",
        ]
    )
    return last_dm
