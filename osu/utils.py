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

from io import BytesIO
from math import trunc

import discord
from emoji import UNICODE_EMOJI_ENGLISH
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_number, humanize_timedelta


def api_is_set():
    async def predicate(self):
        if not await osu_api_key(self):
            return False
        else:
            return True

    return commands.check(predicate)


class Emoji(commands.EmojiConverter):
    async def convert(self, ctx: commands.Context, argument: str):
        if argument in UNICODE_EMOJI_ENGLISH:
            return argument
        return str(await super().convert(ctx, argument))


async def osu_api_key(self):
    return (await self.bot.get_shared_api_tokens("osu")).get("api_key")


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
    api_key = await osu_api_key(self)
    if not username:
        username = await self.config.user(ctx.author).username()
        if not username:
            p = ctx.clean_prefix
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

    player = await get_osu_user(self, ctx, username)
    if player:
        async with self.session.get(f"https://a.ppy.sh/{player['user_id']}") as image:
            image = await image.read()
        filename = player["username"] + ".png"
        avatar = discord.File(BytesIO(image), filename=filename)
        return avatar, filename


async def send_osu_user_info(self, ctx, username: str = None, m: int = 0):
    """osu! User Info Embed"""

    player = await get_osu_user(self, ctx, username, m)
    if player:
        avatar, filename = await get_osu_avatar(self, ctx, username)
        ssh, ss, sh, s, a = await rank_emojis(self)

        # Inspired by owo#0498 (Thanks Stevy 😹)
        description = (
            "**▸ Joined at:** {}\n"
            "**▸ Rank:** #{} (:flag_{}: #{})\n"
            "**▸ Level:** {}\n"
            "**▸ PP:** {}\n"
            "**▸ Accuracy:** {}%\n"
            "**▸ Playcount:** {}\n"
            "**▸ Playtime:** {}\n"
            "**▸ Ranks:** {}`{}` {}`{}` {}`{}` {}`{}` {}`{}`\n"
            "**▸ Ranked Score:** {}\n"
            "**▸ Total Score:** {}"
        ).format(
            player["join_date"][:10],
            humanize_number(player["pp_rank"]),
            player["country"].lower(),
            humanize_number(player["pp_country_rank"]),
            trunc(float(player["level"])),
            humanize_number(round(float(player["pp_raw"]))),
            round(float(player["accuracy"]), 2),
            humanize_number(player["playcount"]),
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
            humanize_number(player["ranked_score"]),
            humanize_number(player["total_score"]),
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
