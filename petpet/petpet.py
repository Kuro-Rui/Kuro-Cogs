"""
MIT License

Copyright (c) 2020-present phenom4n4n

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
import math
from io import BytesIO

import discord
import kuroutils
from PIL import Image
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path


class PetPet(kuroutils.Cog):
    """Make PetPet GIFs!"""

    __author__ = ["PhenoM4n4n", "Kuro"]
    __version__ = "0.0.2"

    def __init__(self, bot: Red):
        super().__init__(bot)

    @commands.bot_has_permissions(attach_files=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(cooldown_after_parsing=True)
    async def petpet(self, ctx, *, user: discord.User = commands.Author):
        """PetPet someone."""
        async with ctx.typing():
            avatar = await self.get_avatar(user)
            task = functools.partial(self.gen_petpet, avatar)
            image = await self.generate_image(task)
        if isinstance(image, str):
            await ctx.send(image)
        else:
            await ctx.send(file=image)

    async def get_avatar(self, user: discord.User) -> BytesIO:
        avatar = BytesIO()
        await user.avatar.save(avatar, seek_begin=True)
        return avatar

    def bytes_to_image(self, image: BytesIO, size: int) -> Image:
        new = Image.open(image).convert("RGBA")
        new = new.resize((size, size), Image.Resampling.LANCZOS)
        image.close()
        return new

    def gen_petpet(self, avatar: BytesIO) -> discord.File:
        avatar = self.bytes_to_image(avatar, 75)
        # Base canvas
        sprite = Image.open(f"{bundled_data_path(self)}/sprite.png", mode="r").convert("RGBA")
        # Pasting the pfp with a patting and squishing effect
        images = []
        for index in range(5):
            im = Image.new("RGBA", (100, 100), None)
            # Calculate the vertical offset to create a patting effect
            patting_offset = int(5 * math.sin(2 * math.pi * index / 5))
            # Calculate the horizontal scale to create the squishy effect
            horizontal_scale = 1.0 + 0.1 * math.sin(2 * math.pi * index / 5)
            avatar_squished = avatar.resize((int(75 * horizontal_scale), 75))
            im.paste(
                avatar_squished,
                (25 - (avatar_squished.width - 75) // 2, 25 - patting_offset),
                avatar_squished,
            )
            im.paste(sprite, (0 - (112 * index), 0), sprite)
            images.append(im)
        sprite.close()
        avatar.close()
        # Set the duration for each frame to 50 milliseconds
        durations = [50] * len(images)
        fp = BytesIO()
        images[0].save(
            fp,
            "GIF",
            save_all=True,
            append_images=images[1:],
            loop=0,
            disposal=2,
            duration=durations,
        )
        fp.seek(0)
        for im in images:
            im.close()
        file = discord.File(fp, "petpet.gif")
        fp.close()
        return file

    async def generate_image(self, task: functools.partial):
        task = self.bot.loop.run_in_executor(None, task)
        try:
            image = await asyncio.wait_for(task, timeout=60)
        except asyncio.TimeoutError:
            return "An error occurred while generating this image. Try again later."
        else:
            return image


"""
        files = []
        for im in images:
            fp = BytesIO()
            im.save(fp, "PNG")
            fp.seek(0)
            files.append(fp)
            fp.close()
        fp = BytesIO()
        imageio.mimsave(fp, images, "gif")
        fp.seek(0)
        _file = discord.File(fp, "petpet.gif")
        fp.close()
        return [_file]

        files = []
        for im in images:
            fp = BytesIO()
            im.save(fp, "PNG")
            fp.seek(0)
            _file = discord.File(fp, "petpet.png")
            fp.close()
            files.append(_file)
        return files

        fp = BytesIO()
        images[0].save(
            fp,
            "GIF",
            save_all=True,
            append_images=images[1:],
            loop=0,
            disposal=2,
        )
        fp.seek(0)
        for im in images:
            im.close()
        _file = discord.File(fp, "petpet.gif")
        fp.close()
        return _file
"""
