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
import datetime

import aiohttp
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list


class ImgBB(commands.Cog):
    """Upload an image to ImgBB!"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    def cog_unload(self):
        asyncio.create_task(self.session.close())

    @commands.group()
    async def imgbb(self, ctx):
        """Base commands of ImgBB cog."""
        pass

    @commands.is_owner()
    @imgbb.command(aliases=["setcreds"])
    async def creds(self, ctx):
        """Instructions to set ImgBB API Key."""
        embed = discord.Embed(color=await ctx.embed_color())
        embed.description = (
            "1. Go to https://imgbb.com/ and login,\n"
            '2. Go to https://api.imgbb.com/ and press "Add API key",\n'
            "3. Copy the key and set it with `{p}set api imgbb api_key <api_key>`,\n"
            "4. You're all set! Get started with `{p}imgbb upload`."
        ).format(p=ctx.clean_prefix)
        await ctx.send(embed=embed)

    @imgbb.command()
    async def upload(self, ctx, url_or_attachment: str = None, name: str = None):
        """
        Upload an image to imgbb!
        You can provide an url/attachment
        """
        api_key = (await self.bot.get_shared_api_tokens("imgbb")).get("api_key")
        if not api_key:
            return await ctx.send(
                "The ImgBB API key hasn't been set yet! Run `{}imgbb creds` for instructions!".format(
                    ctx.clean_prefix
                )
            )

        if ctx.message.attachments:
            image = ctx.message.attachments[0].url
        else:
            image = url_or_attachment

        if not image:
            return await ctx.send_help()

        if name:
            params = {"name": name, "image": image, "key": api_key}
        else:
            if ctx.message.attachments:
                if "https://" or "http://" not in url_or_attachment:
                    if url_or_attachment:
                        name = url_or_attachment
                        params = {"name": name, "image": image, "key": api_key}
                    else:
                        params = {"image": image, "key": api_key}
            else:
                params = {"image": image, "key": api_key}

        async with ctx.typing():
            async with self.session.post(
                "https://api.imgbb.com/1/upload", params=params
            ) as response:
                ibb = await response.json()
                if response.status == 200:
                    url = ibb["data"]["url"]
                    embed = discord.Embed(title="Here's Your Link!", color=await ctx.embed_color())
                    embed.description = url
                    embed.set_image(url=url)
                    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("There's an error with the API")
