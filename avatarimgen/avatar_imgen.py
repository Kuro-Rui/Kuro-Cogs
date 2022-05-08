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
    __version__ = "1.0.2"

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

    @commands.command(aliases=["ads"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ad(self, ctx, user: discord.User = None):
        """Make an advertisement!"""

        if not user:
            user = ctx.author

        avatar = user.avatar_url_as(format="png")

        async with ctx.typing():
            async with self.session.get(f"https://api.popcat.xyz/ad?image={avatar}") as r:
                embed = discord.Embed(title="Advertisement", color=user.color)
                file = discord.File(BytesIO(await r.read()), filename=f"ads.png")
                embed.set_image(url="attachment://ads.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clown(self, ctx, user: discord.User):  # You don't want to be a clown, do you?
        """This person is a clown, Star."""

        avatar = user.avatar_url_as(format="png")

        async with ctx.typing():
            async with self.session.get(f"https://api.popcat.xyz/clown?image={avatar}") as r:
                embed = discord.Embed(title="Clown", color=user.color)
                file = discord.File(BytesIO(await r.read()), filename=f"clown.png")
                embed.set_image(url="attachment://clown.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def drip(self, ctx, user: discord.User = None):
        """Pretend to wear a rich jacket!"""

        if not user:
            user = ctx.author

        avatar = user.avatar_url_as(format="png")

        async with ctx.typing():
            async with self.session.get(f"https://api.popcat.xyz/drip?image={avatar}") as r:
                embed = discord.Embed(title="Drip", color=user.color)
                file = discord.File(BytesIO(await r.read()), filename=f"drip.png")
                embed.set_image(url="attachment://drip.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gun(self, ctx, user: discord.User = None):
        """Add a gun overlay to your avatar!"""

        if not user:
            user = ctx.author

        avatar = user.avatar_url_as(format="png")

        async with ctx.typing():
            async with self.session.get(f"https://api.popcat.xyz/gun?image={avatar}") as r:
                embed = discord.Embed(title="Gun", color=user.color)
                file = discord.File(BytesIO(await r.read()), filename=f"gun.png")
                embed.set_image(url="attachment://gun.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    @commands.command(aliases=["jokesoverhead"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jokeoverhead(self, ctx, user: discord.User):  # You understand jokes, don't you?
        """This person doesn't get jokes at all!"""

        # The API isn't accepting "?size=1024" part that's attached to avatar URLs
        avatar = f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png"

        async with ctx.typing():
            async with self.session.get(
                f"https://api.popcat.xyz/jokeoverhead?image={avatar}"
            ) as r:
                embed = discord.Embed(title="Jokes Overhead", color=user.color)
                file = discord.File(BytesIO(await r.read()), filename=f"jokeoverhead.png")
                embed.set_image(url="attachment://jokeoverhead.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def mnm(self, ctx, user: discord.User = None):
        """Make anyone turns into a shape of M&M!"""

        if not user:
            user = ctx.author

        avatar = user.avatar_url_as(format="png")

        async with ctx.typing():
            async with self.session.get(f"https://api.popcat.xyz/mnm?image={avatar}") as r:
                embed = discord.Embed(title="M&M", color=user.color)
                file = discord.File(BytesIO(await r.read()), filename=f"mnm.png")
                embed.set_image(url="attachment://mnm.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    @commands.command(aliases=["wall"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uncover(self, ctx, user: discord.User = None):
        """So this person was hiding behind the wall all the time?"""

        if not user:
            user = ctx.author

        avatar = user.avatar_url_as(format="png")

        async with ctx.typing():
            async with self.session.get(f"https://api.popcat.xyz/uncover?image={avatar}") as r:
                embed = discord.Embed(title="Behind The Wall", color=user.color)
                file = discord.File(BytesIO(await r.read()), filename=f"wall.png")
                embed.set_image(url="attachment://wall.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wanted(self, ctx, user: discord.User = None):
        """Make a wanted poster!"""

        if not user:
            user = ctx.author

        avatar = user.avatar_url_as(format="png")

        async with ctx.typing():
            async with self.session.get(f"https://api.popcat.xyz/wanted?image={avatar}") as r:
                embed = discord.Embed(title="WANTED", color=user.color)
                file = discord.File(BytesIO(await r.read()), filename=f"wanted.png")
                embed.set_image(url="attachment://wanted.png")
                pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                await ctx.send(embed=embed, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whowouldwin(self, ctx, user_1: discord.User, user_2: discord.User = None):
        """Who would win?"""

        if not user_2:
            user_2 = ctx.author

        avatar_1 = user_1.avatar_url_as(format="png")
        avatar_2 = user_2.avatar_url_as(format="png")

        if user_1 == user_2:
            await ctx.send("Of course you would tie against yourself.")
        else:
            async with ctx.typing():
                async with self.session.get(
                    f"https://api.popcat.xyz/whowouldwin?image1={avatar_1}&image2={avatar_2}"
                ) as r:
                    embed = discord.Embed(title="Who Would Win?", color=await ctx.embed_color())
                    file = discord.File(BytesIO(await r.read()), filename=f"whowouldwin.png")
                    embed.set_image(url="attachment://whowouldwin.png")
                    pop_cat = "https://c.tenor.com/BT8I5b35oMQAAAAC/oatmeal-meme.gif"
                    embed.set_footer(text="Powered by api.popcat.xyz", icon_url=pop_cat)
                    await ctx.send(embed=embed, file=file)
