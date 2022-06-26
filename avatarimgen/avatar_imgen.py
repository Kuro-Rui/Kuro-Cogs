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
import random
from io import BytesIO

import aiohttp
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list


class AvatarImgen(commands.Cog):
    """Make images from avatars!"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.0.4"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        asyncio.create_task(self.session.close())

    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["ads"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ad(self, ctx, user: discord.User = None):
        """Make an advertisement!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "ad", avatar, title="Advertisement")

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clown(self, ctx, user: discord.User = None):
        """This person is a clown, Star."""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "clown", avatar, title="Clown", color=user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def drip(self, ctx, user: discord.User = None):
        """Pretend to wear a rich jacket!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "drip", avatar, title="Drip", color=user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gun(self, ctx, user: discord.User = None):
        """Add a gun overlay to your avatar!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "gun", avatar, title="Gun", color=user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["jokesoverhead"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jokeoverhead(self, ctx, user: discord.User):  # You understand jokes, don't you?
        """This person doesn't get jokes at all!"""

        # The API isn't accepting "?size=1024" part that's attached to avatar URLs
        avatar = f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png"
        await self.send_embed(ctx, "jokeoverhead", avatar, title="Joke Overhead", color=user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["wall"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uncover(self, ctx, user: discord.User = None):
        """So this person was hiding behind the wall all the time?"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "uncover", avatar, title="Behind The Wall", color=user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wanted(self, ctx, user: discord.User = None):
        """Make a wanted poster!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "wanted", avatar, title="WANTED", color=user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whowouldwin(self, ctx, user_1: discord.User, user_2: discord.User = None):
        """Who would win?"""

        user_2 = user_2 or ctx.author
        if user_1 == user_2:
            return await ctx.send("Of course you would tie against yourself.")
        avatar_1 = str(user_1.avatar_url_as(format="png"))
        avatar_2 = str(user_2.avatar_url_as(format="png"))
        color = random.choice([user_1.color, user_2.color])
        async with ctx.typing():
            async with self.session.get(
                f"https://api.popcat.xyz/whowouldwin?image1={avatar_1}&image2={avatar_2}"
            ) as r:
                embed = discord.Embed(title="Who Would Win?", color=color)
                file = discord.File(BytesIO(await r.read()), filename="whowouldwin.png")
                embed.set_image(url="attachment://whowouldwin.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    async def generate_image(self, ctx, endpoint: str, avatar: str) -> discord.File:
        """Generate an image from the user's avatar."""
        async with ctx.typing():
            async with self.session.get(
                f"https://api.popcat.xyz/{endpoint}", params={"image": avatar}
            ) as r:
                if r.status != 200:
                    return await ctx.send("Something went wrong with the API, try again later.")
                image = await r.read()
        file = BytesIO(image)
        return discord.File(file, filename=f"{endpoint}.png")

    async def send_embed(self, ctx, endpoint: str, avatar: str, **kwargs) -> discord.Message:
        """Send an embed with the generated image."""
        embed = discord.Embed(**kwargs)
        pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
        embed.set_image(url=f"attachment://{endpoint}.png")
        embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
        await ctx.send(embed=embed, file=await self.generate_image(ctx, endpoint, avatar))
