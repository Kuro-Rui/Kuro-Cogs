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
from typing import Literal, Optional

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
    __version__ = "0.1.1"

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
        await self.send_embed(ctx, "popcat", "ad", avatar, "Advertisement", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clown(self, ctx, user: discord.User = None):
        """This person is a clown, Star."""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "popcat", "clown", avatar, "Clown", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def communist(self, ctx, user: discord.User = None):
        """Generate a communist comrade avatar!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "sra", "comrade", avatar, "Communist", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def drip(self, ctx, user: discord.User = None):
        """Pretend to wear a rich jacket!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "popcat", "drip", avatar, "Drip", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gun(self, ctx, user: discord.User = None):
        """Add a gun overlay to your avatar!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "popcat", "gun", avatar, "Gun", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hornylicense(self, ctx, user: discord.User = None):
        """Assign someone a horny license!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "sra", "horny", avatar, "You're Now Legally Horny", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jail(self, ctx, user: discord.User = None):
        """Send someone to jail!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "sra", "jail", avatar, "Go to Jail", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command(alias=["lolipolice"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lolice(self, ctx, user: discord.User = None):
        """Be a loli police and put lolicons to jail!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "sra", "lolice", avatar, "Lolice Chief", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command(alias=["passed"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def missionpassed(self, ctx, user: discord.User = None):
        """Mission passed, respect +100."""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "sra", "passed", avatar, "Mission Passed", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def simpcard(self, ctx, user: discord.User = None):
        """Assign someone a simp card!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "sra", "simpcard", avatar, "You're Now A Simp", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["itssostupid"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sostupid(self, ctx, user: Optional[discord.User], *, message: str):
        """Oh no, it's so stupid!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        async with ctx.typing():
            async with self.session.get(
                "https://some-random-api.ml/canvas/its-so-stupid",
                params={"avatar": avatar, "dog": message},
            ) as r:
                if r.status != 200:
                    return
                file = discord.File(BytesIO(await r.read()), filename="so-stupid.png")
        embed = discord.Embed(title="Oh No, It's So Stupid", color=user.color)
        embed.set_image(url="attachment://so-stupid.png")
        embed.set_footer(
            text="Powered by some-random-api.ml", icon_url="https://i.some-random-api.ml/logo.png"
        )
        await ctx.send(embed=embed, file=file)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tweet(self, ctx, user: Optional[discord.User], *, message: str):
        """Generate a fake Twitter tweet!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        async with ctx.typing():
            params = {
                "avatar": avatar,
                "comment": message,
                "displayname": user.display_name,
                "username": user.name,
            }
            async with self.session.get(
                "https://some-random-api.ml/canvas/tweet", params=params
            ) as r:
                if r.status != 200:
                    return
                file = discord.File(BytesIO(await r.read()), filename="tweet.png")
        embed = discord.Embed(title="Tweet", color=user.color)
        embed.set_image(url="attachment://tweet.png")
        embed.set_footer(
            text="Powered by some-random-api.ml", icon_url="https://i.some-random-api.ml/logo.png"
        )
        await ctx.send(embed=embed, file=file)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["wall"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uncover(self, ctx, user: discord.User = None):
        """So this person was hiding behind the wall all the time?"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "popcat", "uncover", avatar, "Behind The Wall", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wanted(self, ctx, user: discord.User = None):
        """Make a wanted poster!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "popcat", "wanted", avatar, "WANTED", user.color)

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wasted(self, ctx, user: discord.User = None):
        """Wasted."""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        await self.send_embed(ctx, "sra", "wasted", avatar, "Wasted", user.color)

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

    @commands.bot_has_permissions(attach_files=True)
    @commands.command(aliases=["youtubecomment"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ytcomment(self, ctx, user: Optional[discord.User], *, comment: str):
        """Generate a fake YouTube comment!"""

        user = user or ctx.author
        avatar = str(user.avatar_url_as(format="png"))
        async with ctx.typing():
            async with self.session.get(
                "https://some-random-api.ml/canvas/youtube-comment",
                params={"avatar": avatar, "comment": comment, "username": user.display_name},
            ) as r:
                if r.status != 200:
                    return
                file = discord.File(BytesIO(await r.read()), filename="youtube-comment.png")
        embed = discord.Embed(title="YouTube Comment", color=user.color)
        embed.set_image(url="attachment://youtube-comment.png")
        embed.set_footer(
            text="Powered by some-random-api.ml", icon_url="https://i.some-random-api.ml/logo.png"
        )
        await ctx.send(embed=embed, file=file)

    async def generate_image(
        self, ctx, which: Literal["popcat", "sra"], endpoint: str, avatar: str
    ) -> discord.File:
        """Generate image and return a discord.File object."""
        async with ctx.typing():
            if which == "popcat":
                link, params = f"https://api.popcat.xyz/{endpoint}", {"image": avatar}
            elif which == "sra":
                link, params = f"https://some-random-api.ml/canvas/{endpoint}", {"avatar": avatar}
            async with self.session.get(link, params=params) as r:
                if r.status != 200:
                    return
                file = BytesIO(await r.read())
        return discord.File(file, filename=f"{endpoint}.png")

    async def send_embed(
        self,
        ctx,
        which: Literal["popcat", "sra"],
        endpoint: str,
        avatar: str,
        title: str,
        color: discord.Color,
    ) -> discord.Message:
        """Send an embed with the generated image."""
        file = await self.generate_image(ctx, which, endpoint, avatar)
        if not file:
            return await ctx.send("Something went wrong with the API, try again later.")
        if which == "popcat":
            by = "api.popcat.xyz"
            icon_url = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
        elif which == "sra":
            by = "some-random-api.ml"
            icon_url = "https://i.some-random-api.ml/logo.png"
        embed = discord.Embed(title=title, color=color)
        embed.set_image(url=f"attachment://{endpoint}.png")
        embed.set_footer(text=f"Powered by {by}", icon_url=icon_url)
        await ctx.send(embed=embed, file=file)
