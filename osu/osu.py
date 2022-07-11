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
from redbot.core.utils.chat_formatting import humanize_list, humanize_number, humanize_timedelta

from .converters import Emoji
from .utils import api_is_set, osu_api_key


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
    __version__ = "3.1.1"

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
            player = await self.get_osu_user(ctx, username)
            if player:
                username = player["username"]
                await self.config.user(ctx.author).username.set(username)
                await ctx.tick()
                await ctx.send(f"Your username has been set to `{username}`.")

    @api_is_set()
    @osuset.group()
    @commands.is_owner()
    @commands.bot_has_permissions(use_external_emojis=True)
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
        await ctx.send(f"The custom emoji for SSH Rank has been set to: {ssh_emoji}")

    @emoji.command()
    async def ss(self, ctx, ss_emoji: Optional[Emoji]):
        """Set custom emoji for SS rank."""
        if not ss_emoji:
            await self.config.ss_emoji.clear()
            await ctx.send("The custom emoji for SS Rank has been removed.")
        else:
            await self.config.ss_emoji.set(ss_emoji)
        await ctx.send(f"The custom emoji for SS Rank has been set to: {ss_emoji}")

    @emoji.command()
    async def sh(self, ctx, sh_emoji: Optional[Emoji]):
        """Set custom emoji for SH rank."""
        if not sh_emoji:
            await self.config.sh_emoji.clear()
            await ctx.send("The custom emoji for SH Rank has been removed.")
        else:
            await self.config.sh_emoji.set(sh_emoji)
        await ctx.send(f"The custom emoji for SH Rank has been set to: {sh_emoji}")

    @emoji.command()
    async def s(self, ctx, s_emoji: Optional[Emoji]):
        """Set custom emoji for S rank."""
        if not s_emoji:
            await self.config.s_emoji.clear()
            await ctx.send("The custom emoji for S Rank has been removed.")
        else:
            await self.config.s_emoji.set(s_emoji)
        await ctx.send(f"The custom emoji for S Rank has been set to: {s_emoji}")

    @emoji.command()
    async def a(self, ctx, a_emoji: Optional[Emoji]):
        """Set custom emoji for A rank."""
        if not a_emoji:
            await self.config.a_emoji.clear()
            await ctx.send("The custom emoji for A Rank has been removed.")
        else:
            await self.config.a_emoji.set(a_emoji)
        await ctx.send(f"The custom emoji for A Rank has been set to: {a_emoji}")

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
        await ctx.send("The custom emojis for all ranks has been set.")

    @emoji.command()
    async def current(self, ctx):
        """Shows current set emojis."""
        emojis = [e for e in (await self.config.all()).values()]
        if not emojis:
            return await ctx.send("You haven't set any emojis yet.")
        embed = discord.Embed(title="Current Emojis", color=await ctx.embed_color())
        embed.description = (
            f"`SSH Emoji` : {emojis[0]}\n"
            f"`SS  Emoji` : {emojis[1]}\n"
            f"`SH  Emoji` : {emojis[2]}\n"
            f"`S   Emoji` : {emojis[3]}\n"
            f"`A   Emoji` : {emojis[4]}"
        )
        await ctx.send(embed=embed)

    @emoji.command()
    @commands.bot_has_permissions()
    async def clear(self, ctx):
        """Clear all set custom emojis for ranks."""
        await self.config.clear()
        await ctx.send("All custom emojis for ranks has been cleared.")

    @api_is_set()
    @commands.command()
    @commands.bot_has_permissions(attach_files=True)
    async def osuavatar(self, ctx, *, username: Optional[str]):
        """Shows your/another user osu! Avatar"""
        if not username:
            username = await self.config.user(ctx.author).username()
        player = await self.get_osu_user(ctx, username)
        if player:
            avatar, filename = await self.get_osu_avatar(ctx, player["username"])
            embed = discord.Embed(color=await ctx.embed_color())
            embed.set_author(
                name="{}'s osu! Avatar".format(player["username"]),
                url="https://a.ppy.sh/{}".format(player["user_id"]),
            )
            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(embed=embed, file=avatar)

    @api_is_set()
    @commands.command(aliases=["osu", "std"])
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def standard(self, ctx, *, username: Optional[str]):
        """Shows an osu!standard User Stats!"""

        await self.send_osu_user_info(ctx, username, 0)

    @api_is_set()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def taiko(self, ctx, *, username: Optional[str]):
        """Shows an osu!taiko User Stats!"""

        await self.send_osu_user_info(ctx, username, 1)

    @api_is_set()
    @commands.command(aliases=["ctb", "catchthebeat"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def catch(self, ctx, *, username: Optional[str]):
        """Shows an osu!catch User Stats!"""

        await self.send_osu_user_info(ctx, username, 2)

    @api_is_set()
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def mania(self, ctx, *, username: Optional[str]):
        """Shows an osu!mania User Stats!"""

        await self.send_osu_user_info(ctx, username, 3)

    @api_is_set()
    @commands.command(aliases=["osuc", "osuimage", "osuimg"])
    @commands.cooldown(60, 60, commands.BucketType.default)
    @commands.bot_has_permissions(attach_files=True)
    async def osucard(self, ctx, *, username: Optional[str]):
        """Shows an osu!standard User Card!"""  # Thanks Epic, thanks Preda <3
        player = await self.get_osu_user(ctx, username)
        if player:
            async with self.session.get(
                "https://api.martinebot.com/v1/imagesgen/osuprofile",
                params={"player_username": player["username"]},
            ) as response:
                if response.status == 201:
                    card = await response.read()
                elif response.status in [404, 410, 422]:
                    return await ctx.send((await response.json())["message"])
                else:
                    return await ctx.send("API is currently down, please try again later.")
            embed = discord.Embed(color=await ctx.embed_color())
            embed.set_author(
                name="{}'s osu! Standard Card:".format(player["username"]),
                url="https://osu.ppy.sh/users/{}".format(player["user_id"]),
            )
            filename = player["username"].replace(" ", "_") + ".png"
            file = discord.File(BytesIO(card), filename)
            embed.set_image(url=f"attachment://{filename}")
            embed.set_footer(
                text="Powered by api.martinebot.com",
                icon_url="https://img.icons8.com/color/48/000000/osu.png",
            )
            await ctx.send(embed=embed, file=file)

    async def rank_emojis(self):
        """Rank Emojis"""

        ssh_emoji = await self.config.ssh_emoji()
        ssh = f"{ssh_emoji} " if ssh_emoji else "**SSH** "

        ss_emoji = await self.config.ss_emoji()
        ss = f"{ss_emoji} " if ss_emoji else "**SS** "

        sh_emoji = await self.config.sh_emoji()
        sh = f"{sh_emoji} " if sh_emoji else "**SH** "

        s_emoji = await self.config.s_emoji()
        s = f"{s_emoji} " if s_emoji else "**S** "

        a_emoji = await self.config.a_emoji()
        a = f"{a_emoji} " if a_emoji else "**A** "

        return ssh, ss, sh, s, a

    async def get_osu_user(self, ctx, username: str = None, m: int = 0):
        """osu! API Call"""
        if not username:
            username = await self.config.user(ctx.author).username()
            if not username:
                p = ctx.prefix
                command = ctx.invoked_with
                error_title = "Your username hasn't been set yet!"
                error_desc = (
                    f"You can set it with `{p}osuset username <username>`\n"
                    f"You can also provide a username: `{p}{command} <username>`"
                )
                error_embed = discord.Embed(
                    title=error_title, description=error_desc, color=await ctx.embed_color()
                )
                await ctx.send(embed=error_embed)
                return

        api_key = await osu_api_key(ctx)
        async with self.session.post(
            f"https://osu.ppy.sh/api/get_user?k={api_key}&u={username}&m={m}"
        ) as response:
            osu = await response.json()
        if osu:
            return osu[0]
        else:
            await ctx.send("Player not found.")
            return

    async def get_osu_avatar(self, ctx, username: str = None):
        """Get an osu! Avatar"""
        player = await self.get_osu_user(ctx, username)
        if player:
            async with self.session.get(f"https://a.ppy.sh/{player['user_id']}") as image:
                avatar = await image.read()
            filename = player["username"].replace(" ", "_") + ".png"
            avatar = discord.File(BytesIO(avatar), filename=filename)
            return avatar, filename

    async def send_osu_user_info(self, ctx, username: str = None, m: int = 0):
        """osu! User Info Embed"""
        player = await self.get_osu_user(ctx, username, m)
        if player:
            avatar, filename = await self.get_osu_avatar(ctx, username)
            ssh, ss, sh, s, a = await self.rank_emojis()

            # Inspired by owo#0498 (Thanks Stevy 😹)
            description = (
                "▸ **Joined at:** {}\n"
                "▸ **Rank:** #{} (:flag_{}: #{})\n"
                "▸ **Level:** {}\n"
                "▸ **PP:** {}\n"
                "▸ **Accuracy:** {}%\n"
                "▸ **Playcount:** {}\n"
                "▸ **Playtime:** {}\n"
                "▸ **Ranks:** {}`{}` {}`{}` {}`{}` {}`{}` {}`{}`\n"
                "▸ **Ranked Score:** {}\n"
                "▸ **Total Score:** {}"
            ).format(
                player["join_date"][:10],
                humanize_number(int(player["pp_rank"])),
                player["country"].lower(),
                humanize_number(int(player["pp_country_rank"])),
                round(float(player["level"]), 2),
                humanize_number(round(float(player["pp_raw"]))),
                round(float(player["accuracy"]), 2),
                humanize_number(int(player["playcount"])),
                humanize_timedelta(seconds=player["total_seconds_played"]),
                ssh,
                player["count_rank_ssh"],
                ss,
                player["count_rank_ss"],
                sh,
                player["count_rank_sh"],
                s,
                player["count_rank_s"],
                a,
                player["count_rank_a"],
                humanize_number(int(player["ranked_score"])),
                humanize_number(int(player["total_score"])),
            )

            if m == 0:
                type = icon = "osu"
                mode = "Standard"
            elif m == 1:
                type = icon = "taiko"
                mode = "Taiko"
            elif m == 2:
                type = "fruits"
                icon = "ctb"
                mode = "Catch"
            elif m == 3:
                type = icon = "mania"
                mode = "Mania"

            embed = discord.Embed(description=description, color=await ctx.embed_color())
            embed.set_author(
                icon_url="https://lemmmy.pw/osusig/img/{}.png".format(icon),
                url="https://osu.ppy.sh/users/{}/{}".format(player["user_id"], type),
                name="osu! {} Profile for {}".format(mode, player["username"]),
            )
            embed.set_footer(
                text="Powered by osu!", icon_url="https://img.icons8.com/color/48/000000/osu.png"
            )
            embed.set_thumbnail(url=f"attachment://{filename}")
            await ctx.send(embed=embed, file=avatar)
