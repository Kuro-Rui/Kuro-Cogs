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
import importlib
import sys
from typing import Optional

import aiohttp
import discord
import kuroutils
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import bold, escape, humanize_list, inline
from redbot.core.utils.views import ConfirmView, SetApiView


class KuroTools(kuroutils.Cog):
    """Just some (maybe) useful tools made by Kuro."""

    __author__ = ["Kuro"]
    __version__ = "0.0.1"

    def __init__(self, bot: Red) -> None:
        super().__init__(bot)
        self.session = aiohttp.ClientSession()

    async def cog_unload(self) -> None:
        super().cog_unload()
        await self.session.close()

    @commands.command()
    async def raw(self, ctx: commands.Context, message: Optional[discord.Message] = None):
        """
        Get a raw content from a message.

        You can either reply to a message or provide a message ID/Link.
        """
        if not message and not ctx.message.reference:
            return await ctx.send_help()
        if ctx.message.reference:
            content = ctx.message.reference.resolved.content
            ctx.message.reference = None
            return await ctx.send(escape(content, mass_mentions=True, formatting=True))
        if message:
            if not message.content:
                return await ctx.send("Cannot send an empty message.")
            await ctx.send(escape(message.content, mass_mentions=True, formatting=True))

    # Thanks AAA3A!
    @commands.is_owner()
    @commands.command()
    async def reloadmodule(self, ctx: commands.Context, module: str):
        """
        Force reload a module from `sys.modules`.

        Please only use this if you know what you're doing :p
        """
        modules = sorted([m for m in sys.modules if m.split(".")[0] == module], reverse=True)
        if not modules:
            await ctx.send("I couldn't find a module with that name.")
            return
        formatted = humanize_list([inline(m) for m in modules])
        view = ConfirmView(ctx.author)
        view.message = await ctx.send(f"Are you sure you want to reload {formatted}?", view=view)
        await view.wait()
        if view.result:
            for module in modules:
                importlib.reload(sys.modules[module])
            await ctx.send(f"Reloaded {formatted}.")
        else:
            await ctx.send("Cancelled.")

    @commands.group(aliases=["wof"])
    @commands.cooldown(3, 1, commands.BucketType.default)
    async def wheeloffortune(self, ctx: commands.Context, arguments: str):
        """
        Play a Wheel of Fortune game!

        You can provide either 2, 3, 4, or 6 arguments. (Split the arguments with |)
        """
        args = arguments.split("|")
        if len(args) not in (2, 3, 4, 6):
            await ctx.send_help()
            return
        key = (await self.bot.get_shared_api_tokens("jeyyapi")).get("api_key")
        if not key:
            await ctx.send("The API key for JeyyAPI is not set.")
            return
        headers = {"Authorization": f"Bearer {key}"}
        params = {"args": args}
        async with self.session.get(
            "https://api.jeyy.xyz/v2/discord/wheel",
            headers=headers,
            params=params,
        ) as response:
            if response.status != 200:
                await ctx.send("Something went wrong, try again later.")
                return
            data = await response.json()
        embed = discord.Embed(title="Wheel of Fortune", description="Spinning...")
        embed.set_thumbnail(url=data["gif_wheel"])
        embed.add_field(name="Description", value=data["desc"].replace("\t\t", " "))
        message = await ctx.send(embed=embed)
        embed.color = data["result_color"]
        embed.description = bold("WE HAVE A WINNER!") + "\n\n" + data["result"]
        embed.set_thumbnail(url=data["result_img"])
        await asyncio.sleep(data["time"])
        message = await kuroutils.edit_message(message, embed=embed)
        if not message:
            await ctx.send(embed=embed)

    @commands.is_owner()
    @wheeloffortune.command(name="creds")
    async def wof_creds(self, ctx: commands.Context):
        """Instructions to set wheel of fortune API key."""
        description = (
            "1. Go to https://api.jeyy.xyz/dashboard/landing and login with your account\n"
            "2. Go to https://api.jeyy.xyz/dashboard\n"
            '3. Click on "Create an app"\n'
            "4. Fill the label with an application name and ID of your choice\n"
            "5. Copy your api key into:\n`{prefix}set api jeyyapi api_key <your_api_key_here>`"
        ).format(prefix=ctx.prefix)
        view = SetApiView("jeyyapi", {"api_key": ""})
        if await ctx.embed_requested():
            embed = discord.Embed(description=description)
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send(description, view=view)
