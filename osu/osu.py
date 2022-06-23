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
from typing import Optional

import aiohttp
import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import humanize_list

from .utils import (
    Emoji,
    api_is_set,
    get_osu_avatar,
    osu_api_key,
    get_osu_user,
    send_osu_user_info,
)


class Osu(commands.Cog):
    """Show osu! user stats with osu! API"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=842364413)
        self.config.register_global(
            ssh_emoji=None, ss_emoji=None, sh_emoji=None, s_emoji=None, a_emoji=None
        )
        self.config.register_user(username=None)
        self.session = aiohttp.ClientSession()

    __author__ = humanize_list(["Kuro"])
    __version__ = "3.1.0"

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

    async def red_delete_data_for_user(self, *, requester, user_id: int):
        await self.config.user_from_id(user_id).clear()

    @commands.group()
    async def osuset(self, ctx):
        """Settings for osu!"""
        pass

    @osuset.command()
    @commands.is_owner()
    async def creds(self, ctx):
        """Instructions to set osu! API Key."""
        embed = discord.Embed(color=await ctx.embed_color())
        embed.description = (
            "How to set osu! API key:\n"
            "1. Go to https://osu.ppy.sh/p/api/ and login.\n"
            "2. Set App Name ({app}) & App URL as https://osu.ppy.sh/api/v1\n(anything can do tho).\n"
            "3. Copy the API Key and set it with `{p}set api osu api_key <API_Key>`.\n"
            "4. Set emojis (SSH, SS, SH, S, A) for the osu! user info (except card) with\n`{p}osuset emoji`"
        ).format(app=ctx.me.name, p=ctx.clean_prefix)
        await ctx.send(embed=embed)

    @api_is_set()
    @osuset.command(aliases=["name"])
    async def username(self, ctx, *, username: str = None):
        """Set your osu! username."""
        if not username:
            if not await self.config.user(ctx.author).username():
                return await ctx.send_help()
            await self.config.user(ctx.author).username.clear()
            await ctx.tick()
            await ctx.send("Your username has been removed.")
        else:
            player = await get_osu_user(self, ctx, username)
            if player:
                username = player["username"]
                await self.config.user(ctx.author).username.set(username)
                await ctx.tick()
                await ctx.send(f"Your username has been set to `{username}`.")

    @api_is_set()
    @osuset.group()
    @commands.is_owner()
    async def emoji(self, ctx):
        """Set custom emoji for ranks."""
        pass

    @emoji.command()
    async def ssh(self, ctx, ssh_emoji: Optional[Emoji]):
        """Set custom emoji for SSH rank."""
        if not ssh_emoji:
            await self.config.ssh_emoji.clear()
            await ctx.send("The custom emoji for SSH Rank has been removed.")
        else:
            await self.config.ssh_emoji.set(ssh_emoji)
        await ctx.send(f"The custom emoji for SSH Rank has been set to: {ssh_emoji}.")

    @emoji.command()
    async def ss(self, ctx, ss_emoji: Optional[Emoji]):
        """Set custom emoji for SS rank."""
        if not ss_emoji:
            await self.config.ss_emoji.clear()
            await ctx.send("The custom emoji for SS Rank has been removed.")
        else:
            await self.config.ss_emoji.set(ss_emoji)
        await ctx.send(f"The custom emoji for SS Rank has been set to: {ss_emoji}.")

    @emoji.command()
    async def sh(self, ctx, sh_emoji: Optional[Emoji]):
        """Set custom emoji for SH rank."""
        if not sh_emoji:
            await self.config.sh_emoji.clear()
            await ctx.send("The custom emoji for SH Rank has been removed.")
        else:
            await self.config.sh_emoji.set(sh_emoji)
        await ctx.send(f"The custom emoji for SH Rank has been set to: {sh_emoji}.")

    @emoji.command()
    async def s(self, ctx, s_emoji: Optional[Emoji]):
        """Set custom emoji for S rank."""
        if not s_emoji:
            await self.config.s_emoji.clear()
            await ctx.send("The custom emoji for S Rank has been removed.")
        else:
            await self.config.s_emoji.set(s_emoji)
        await ctx.send(f"The custom emoji for S Rank has been set to: {s_emoji}.")

    @emoji.command()
    async def a(self, ctx, a_emoji: Optional[Emoji]):
        """Set custom emoji for A rank."""
        if not a_emoji:
            await self.config.a_emoji.clear()
            await ctx.send("The custom emoji for A Rank has been removed.")
        else:
            await self.config.a_emoji.set(a_emoji)
        await ctx.send(f"The custom emoji for A Rank has been set to: {a_emoji}.")

    @emoji.command()
    async def multi(
        self,
        ctx,
        ssh_emoji: Emoji,
        ss_emoji: Emoji,
        sh_emoji: Emoji,
        s_emoji: Emoji,
        a_emoji: Emoji,
    ):
        """Set custom emoji for all ranks at once!"""
        await self.config.ssh_emoji.set(ssh_emoji)
        await self.config.ss_emoji.set(ss_emoji)
        await self.config.sh_emoji.set(sh_emoji)
        await self.config.s_emoji.set(s_emoji)
        await self.config.a_emoji.set(a_emoji)
        await ctx.tick()

    @emoji.command()
    async def clear(self, ctx):
        """Clear all set custom emojis for ranks."""
        await self.config.clear()
        await ctx.tick()
        await ctx.send("All custom emojis for ranks has been cleared.")

    @api_is_set()
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(attach_files=True)
    async def osuavatar(self, ctx, *, username: Optional[str]):
        """Shows your/another user osu! Avatar"""
        if not username:
            username = await self.config.user(ctx.author).username()
        player = await get_osu_user(self, ctx, username=username)
        if player:
            avatar, filename = await get_osu_avatar(self, ctx, player["username"])
            embed = discord.Embed(color=await ctx.embed_color())
            embed.set_author(name="{}'s osu! Avatar".format(player["username"]))
            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(embed=embed, file=avatar)

    @api_is_set()
    @commands.command(aliases=["osu", "std"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def standard(self, ctx, *, username: Optional[str]):
        """Shows an osu!standard User Stats!"""

        await send_osu_user_info(self, ctx, username)

    @api_is_set()
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def taiko(self, ctx, *, username: Optional[str]):
        """Shows an osu!taiko User Stats!"""

        await send_osu_user_info(self, ctx, username, 1)

    @api_is_set()
    @commands.command(aliases=["ctb", "catchthebeat"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def catch(self, ctx, *, username: Optional[str]):
        """Shows an osu!catch User Stats!"""

        await send_osu_user_info(self, ctx, username, 2)

    @api_is_set()
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def mania(self, ctx, *, username: Optional[str]):
        """Shows an osu!mania User Stats!"""

        await send_osu_user_info(self, ctx, username, 3)

    @api_is_set()
    @commands.command(aliases=["osuc", "osuimage", "osuimg"])
    @commands.cooldown(60, 60, commands.BucketType.default)
    @commands.bot_has_permissions(attach_files=True)
    async def osucard(self, ctx, *, username: Optional[str]):
        """Shows an osu!standard User Card!"""  # Thanks Epic, thanks Preda <3
        player = await get_osu_user(self, ctx, username=username)
        if player:
            async with self.session.get(
                "https://api.martinebot.com/v1/imagesgen/osuprofile",
                params={"player_username": player['username']},
            ) as response:
                if response.status == 201:
                    embed = discord.Embed(color=await ctx.embed_color())
                    embed.set_author(
                        name="{}'s osu! Standard Card:".format(player["username"]),
                        url="https://osu.ppy.sh/users/{}".format(player["user_id"]),
                    )
                    filename = player["username"] + ".png"
                    card = discord.File(BytesIO(await response.read()), filename=filename)
                    embed.set_image(url=f"attachment://{filename}")
                    embed.set_footer(
                        text="Powered by api.martinebot.com",
                        icon_url="https://img.icons8.com/color/48/000000/osu.png",
                    )
                    await ctx.send(embed=embed, file=card)
                elif response.status in [404, 410, 422]:
                    await ctx.send((await response.json())["message"])
                else:
                    await ctx.send("API is currently down, please try again later.")
