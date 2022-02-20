import aiohttp
import datetime

import discord
from redbot.core import commands


class ImgBB(commands.Cog):
    """Upload an image to ImgBB!"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.group()
    async def imgbb(self, ctx):
        """Base commands of ImgBB cog."""
        pass

    @imgbb.command(aliases=["setcreds"])
    async def creds(self, ctx):
        """Instructions to set ImgBB API Key."""
        embed = discord.Embed(color=await ctx.embed_color())
        embed.description = (
            "1. Go to https://imgbb.com/ and login,\n"
            "2. Go to https://api.imgbb.com/ and press \"Add API key\",\n"
            "3. Copy the key and set it with `{p}set api imgbb api_key <api_key>`,\n"
            "4. You're all set! Get started with `{p}imgbb upload`."
        ).format(p=self.bot.clean_prefix)
        await ctx.send(embed=embed)

    @imgbb.command()
    async def upload(self, ctx, name: str = None, url_or_attachment: str = None):
        """
        Upload an image to imgbb!
        You can provide an url/attachment
        """
        api_key = (await self.bot.get_shared_api_tokens("imgbb")).get("api_key")
        if not api_key:
            return await ctx.send(
                "The ImgBB API key hasn't been set yet! Run `{}imgbb creds` for instructions!".format(
                    self.bot.clean_prefix
                )
            )

        if name:
            params = {"name": name, "image": url_or_attachment, "key": api_key}
        else:
            params = {"image": url_or_attachment, "key": api_key}

        if not url_or_attachment:
            if ctx.message.attachments:
                url_or_attachment = ctx.message.attachments[0].url
            else:
                return await ctx.send_help()

        if name is not None and url_or_attachment is None:
            if "http://" or "https://" in name:
                url_or_attachment = name

        async with ctx.typing():
            async with self.session.post("https://api.imgbb.com/1/upload", params=params) as response:
                ibb = await response.json()
                if response.status == 200:
                    url = ibb["data"]["url"]
                    embed = discord.Embed(title="Here's Your Link!", color=await ctx.embed_color())
                    embed.description = url
                    embed.set_image(url=url)
                    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                    await ctx.send(embed=embed)
                    