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

import asyncio
import functools
import json
import random
from io import BytesIO
from pathlib import Path

import discord
from PIL import Image
from redbot.core.data_manager import bundled_data_path as image_folder

__all__ = ["generate_fumoroid", "generate_image", "get_avatar", "summon_fumo"]

with open(Path(__file__).parent / "fumos.json") as fumos:
    fumo = json.load(fumos)


async def summon_fumo(ctx, type: str):
    """Summon a Fumo."""
    url = random.choice(fumo[type])
    if type == "Video" or type == "FUMO FRIDAY":
        return await ctx.send("**Here's a Random Fumo Video! ᗜˬᗜ**\n" + url)
    embed = discord.Embed(title=f"Here's a Random Fumo {type}! ᗜˬᗜ", color=await ctx.embed_color())
    embed.set_image(url=url)
    await ctx.send(embed=embed)


def bytes_to_image(image: BytesIO, size: int):
    image = Image.open(image).convert("RGBA")
    image = image.resize((size, size), Image.ANTIALIAS)
    return image


# Thanks Phen
async def get_avatar(user: discord.User):
    avatar = BytesIO()
    await user.avatar_url_as(static_format="png").save(avatar, seek_begin=True)
    return avatar


# Thanks Phen & Glas
def generate_fumoroid(ctx, member_avatar):
    member_avatar = bytes_to_image(member_avatar, 300)
    image = Image.new("RGBA", (451, 600), None)
    fumoroid = Image.open(
        f"{image_folder(ctx.bot.get_cog('Fumo'))}/fumoroid.png", mode="r"
    ).convert("RGBA")
    image.rotate(120, resample=0, expand=False, center=None, translate=None, fillcolor=None)
    image.paste(member_avatar, (150, 200), member_avatar)
    image.paste(fumoroid, (0, 0), fumoroid)
    fumoroid.close()
    member_avatar.close()
    fp = BytesIO()
    image.save(fp, "PNG")
    fp.seek(0)
    image.close()
    file = discord.File(fp, "fumopic.png")
    fp.close()
    return file


# Thanks Phen
async def generate_image(ctx, task: functools.partial):
    task = ctx.bot.loop.run_in_executor(None, task)
    try:
        image = await asyncio.wait_for(task, timeout=60)
    except asyncio.TimeoutError:
        return "An error occurred while generating this image. Try again later."
    else:
        return image
