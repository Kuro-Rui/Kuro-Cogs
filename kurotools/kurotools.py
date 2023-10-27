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
import math
import sys
from pathlib import Path
from typing import Optional

import aiohttp
import discord
import kuroutils
from redbot.cogs.downloader.repo_manager import Repo
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.data_manager import cog_data_path
from redbot.core.utils.chat_formatting import bold, escape, humanize_list, inline
from redbot.core.utils.views import ConfirmView, SetApiView


class KuroTools(kuroutils.Cog):
    """Just some (maybe) useful tools made by Kuro."""

    __author__ = ["Kuro"]
    __version__ = "0.0.5"

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
            await ctx.send_help()
            return
        if ctx.message.reference:
            content = ctx.message.reference.resolved.content
            ctx.message.reference = None
            await ctx.send(escape(content, mass_mentions=True, formatting=True))
            return
        if message:
            if not message.content:
                await ctx.send("Cannot send an empty message.")
                return
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
            content = f"Reloaded {formatted}."
        else:
            content = f"Cancelled."
        message = await kuroutils.edit_message(view.message, content=content)
        if not message:
            await ctx.send(content)

    @commands.is_owner()
    @commands.group()
    async def kuroutils(self, ctx: commands.Context):
        """KuroUtils management commands."""
        pass

    @kuroutils.command(name="update")
    async def kuroutils_update(self, ctx: commands.Context):
        """Update KuroUtils."""
        if not (downloader := self.bot.get_cog("Downloader")):
            await ctx.send("Downloader cog is not loaded.")
            return
        old_version = importlib.metadata.version("Kuro-Utils")
        async with ctx.typing():
            repo = Repo("", "", "", "", Path.cwd())
            lib_path = cog_data_path(downloader) / "lib"
            successful = await repo.install_raw_requirements(
                ["git+https://github.com/Kuro-Rui/Kuro-Utils"], lib_path
            )
            if not successful:
                await ctx.send("Something went wrong, please check your logs for a complete list.")
                return
        modules = sorted([m for m in sys.modules if m.split(".")[0] == "kuroutils"], reverse=True)
        for module in modules:
            importlib.reload(sys.modules[module])
        new_version = importlib.metadata.version("Kuro-Utils")
        await ctx.send(
            "KuroUtils has been updated successfully!\n"
            f"{inline(old_version)} → {inline(new_version)}"
        )

    @kuroutils.command(name="version")
    async def kuroutils_version(self, ctx: commands.Context):
        """Get the version of KuroUtils."""
        await ctx.send(f"KuroUtils v{version('Kuro-Utils')}")

    @commands.group(aliases=["wof"], invoke_without_command=True)
    @commands.cooldown(3, 1, commands.BucketType.default)
    @commands.max_concurrency(1, commands.BucketType.channel)
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
        await asyncio.sleep(math.ceil(data["time"]) + 0.5)
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
