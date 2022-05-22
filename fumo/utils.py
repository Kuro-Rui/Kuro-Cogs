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

from io import BytesIO
import json
from pathlib import Path
import random

import discord

with open(Path(__file__).parent / "fumos.json") as fumos:
    fumo = json.load(fumos)


async def summon_fumo(self, ctx, type: str):
    """Summon a Fumo."""
    url = random.choice(fumo[type])
    if type == "Video" or "FUMO FRIDAY":
        async with self.session.get(url) as response:
            video = discord.File(BytesIO(await response.read()))
        return await ctx.send(embed="**Here's a Random Fumo Video! ᗜˬᗜ**", file=video)
    e = discord.Embed(color=await ctx.embed_color())
    e.title = f"Here's a Random Fumo {type}! ᗜˬᗜ"
    e.set_image(url=url)
    await ctx.send(embed=e)
