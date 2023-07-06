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
from io import BytesIO

import discord
from PIL import Image
from redbot.core.commands import Context
from redbot.core.data_manager import bundled_data_path as data_path


def bytes_to_image(image: BytesIO, size: int):
    image = Image.open(image).convert("RGBA")
    image = image.resize((size, size), Image.ANTIALIAS)
    return image


# Thanks Phen
async def get_avatar(user: discord.User):
    avatar = BytesIO()
    await user.avatar.with_static_format("png").save(avatar, seek_begin=True)
    return avatar


async def generate_image(ctx, task: functools.partial):
    task = ctx.bot.loop.run_in_executor(None, task)
    try:
        image = await asyncio.wait_for(task, timeout=60)
    except asyncio.TimeoutError:
        return "An error occurred while generating this image. Try again later."
    else:
        return image


# Thanks Glas
def generate_fumoroid(ctx: Context, avatar: BytesIO):
    avatar = bytes_to_image(avatar, 300)
    image = Image.new("RGBA", (451, 600), None)
    path = f"{data_path(ctx.bot.get_cog('Fumo'))}/Fumoroid.png"
    fumoroid = Image.open(path, mode="r").convert("RGBA")
    image.rotate(120, resample=0, expand=False, center=None, translate=None, fillcolor=None)
    image.paste(avatar, (150, 200), avatar)
    image.paste(fumoroid, (0, 0), fumoroid)
    fumoroid.close()
    avatar.close()

    fp = BytesIO()
    image.save(fp, "PNG")
    fp.seek(0)
    image.close()
    file = discord.File(fp, "fumoroid.png")
    fp.close()
    return file


def generate_marisafie(ctx: Context, avatar: BytesIO):
    avatar = bytes_to_image(avatar, 750)
    image = Image.new("RGBA", (433, 577), None)
    path = f"{data_path(ctx.bot.get_cog('Fumo'))}/Marisafie.png"
    marisafie = Image.open(path, mode="r").convert("RGBA")
    image.rotate(120, resample=0, expand=0, center=None, translate=None, fillcolor=None)
    image.paste(avatar, (0, 0), avatar)
    image.paste(marisafie, (0, 0), marisafie)
    marisafie.close()
    avatar.close()

    fp = BytesIO()
    image.save(fp, "PNG")
    fp.seek(0)
    image.close()
    file = discord.File(fp, "marisafie.png")
    fp.close()
    return file


def generate_marisahat(ctx: Context, avatar: BytesIO):
    avatar = bytes_to_image(avatar, 262)
    image = Image.new("RGBA", (262, 262), None)
    path = f"{data_path(ctx.bot.get_cog('Fumo'))}/MarisaHat.png"
    marihat = Image.open(path, mode="r").convert("RGBA")
    image.paste(avatar, (0, 0), avatar)
    image.paste(marihat, (0, 0), marihat)
    marihat.close()
    avatar.close()

    fp = BytesIO()
    image.save(fp, "PNG")
    fp.seek(0)
    image.close()
    file = discord.File(fp, "marihat.png")
    fp.close()
    return file
