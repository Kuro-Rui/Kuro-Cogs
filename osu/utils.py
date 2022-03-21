from io import BytesIO

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_number, humanize_timedelta

# ~ ~ ~ ~ ~ Decorator ~ ~ ~ ~ ~

def api_is_set():
    async def predicate(self):
        if not (await self.bot.get_shared_api_tokens("osu")).get("api_key"):
            return False
        else:
            return True
    return commands.check(predicate)

# ~ ~ ~ ~ ~ Functions ~ ~ ~ ~ ~

async def rank_emojis(self):
    """Rank Emojis"""
    maybe_ssh_emoji = self.bot.get_emoji(await self.config.ssh_emoji())
    ssh_emoji = await self.config.ssh_emoji()
    if not maybe_ssh_emoji:
        ssh = f"{ssh_emoji} " if ssh_emoji else "**SSH** "
    else:
        ssh = f"{maybe_ssh_emoji} "
    
    maybe_ss_emoji = self.bot.get_emoji(await self.config.ss_emoji())
    ss_emoji = await self.config.ss_emoji()
    if not maybe_ss_emoji:
        ss = f"{ss_emoji} " if ss_emoji else "**SS** "
    else:
        ss = f"{maybe_ss_emoji} "
    
    maybe_sh_emoji = self.bot.get_emoji(await self.config.sh_emoji())
    sh_emoji = await self.config.sh_emoji()
    if not maybe_sh_emoji:
        sh = f"{sh_emoji} " if sh_emoji else "**SH** "
    else:
        sh = f"{maybe_sh_emoji} "
    
    maybe_s_emoji = self.bot.get_emoji(await self.config.s_emoji())
    s_emoji = await self.config.s_emoji()
    if not maybe_s_emoji:
        s = f"{s_emoji} " if s_emoji else "**S** "
    else:
        s = f"{maybe_s_emoji} "
    
    maybe_a_emoji = self.bot.get_emoji(await self.config.a_emoji())
    a_emoji = await self.config.a_emoji()
    if not maybe_a_emoji:
        a = f"{a_emoji} " if a_emoji else "**A** "
    else:
        a = f"{maybe_a_emoji} "
    
    return ssh, ss, sh, s, a

async def osu_api_call(self, ctx, m: int = 0, username: str = None):
    """osu! API Call"""

    api_key = (await self.bot.get_shared_api_tokens("osu")).get("api_key")

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
            error_embed = discord.Embed(title=error_title, description=error_desc, color=await ctx.embed_color())
            return await ctx.send(embed=error_embed)

    async with self.session.post(f"https://osu.ppy.sh/api/get_user?k={api_key}&u={username}&m={m}") as response:
        osu = await response.json()
    return osu if osu else await ctx.send("No results found for this player.")

    # headers = {"content-type": "application/json", "user-key": api_key}

async def get_osu_avatar(self, ctx, username: str = None):
    """Get an osu! Avatar"""

    osu = await osu_api_call(self, ctx, username=username)
    if not username:
        username = await self.config.user(ctx.author).username()
        if not username:
            return osu
    
    avatar_url = "https://a.ppy.sh/{}".format(osu[0]["user_id"])
    filename = "{}_osu-avatar.png".format(osu[0]["username"])
    async with self.session.get(avatar_url) as image:
        avatar = discord.File(fp=BytesIO(await image.read()), filename=filename)
    return avatar, avatar_url, filename

async def send_osu_user_info(self, ctx, m: int = 0, username: str = None):
    """osu! User Info Embed"""
    
    osu = await osu_api_call(self, ctx, m, username)
    if not username:
        username = await self.config.user(ctx.author).username()
        if not username:
            return osu

    # avatar_url isn't actually used, just to prevent "too many values to unpack"
    avatar, avatar_url, filename = await get_osu_avatar(self, ctx, username)
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
        osu[0]["join_date"][:10], 
        humanize_number(osu[0]["pp_rank"]), osu[0]["country"].lower(), humanize_number(osu[0]["pp_country_rank"]), 
        osu[0]["level"][:2],
        osu[0]["pp_raw"],
        osu[0]["accuracy"][:5],
        humanize_number(osu[0]["playcount"]),
        humanize_timedelta(seconds=osu[0]["total_seconds_played"]),
        ssh, osu[0]["count_rank_ssh"], ss, osu[0]["count_rank_ss"], 
        sh, osu[0]["count_rank_sh"], s, osu[0]["count_rank_s"], a, osu[0]["count_rank_a"],
        humanize_number(osu[0]["ranked_score"]),
        humanize_number(osu[0]["total_score"])
    ).replace(",", ".")

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
        url="https://osu.ppy.sh/users/{}/{}".format(osu[0]["user_id"], type),
        name="osu! {} Profile for {}".format(mode, osu[0]["username"])
    )
    embed.set_footer(text="Powered by osu!", icon_url="https://img.icons8.com/color/48/000000/osu.png")
    embed.set_thumbnail(url=f"attachment://{filename}")
    await ctx.send(embed=embed, file=avatar)

async def send_osu_user_card(self, ctx, username: str = None):
    """Sends an osu! Profile Card from Martine API"""

    osu = await osu_api_call(self, ctx, username=username)
    if not username:
        username = await self.config.user(ctx.author).username()
        if not username:
            return osu

    async with self.session.get(
        "https://api.martinebot.com/v1/imagesgen/osuprofile?player_username={}".format(osu[0]["username"])
    ) as response:
        if response.status in [200, 201]:
            embed = discord.Embed(color=await ctx.embed_color())
            embed.set_author(
                name="{}'s osu! Standard Stats:".format(osu[0]["username"]),
                url="https://osu.ppy.sh/users/{}".format(osu[0]["user_id"])
            )
            filename = "{}_osu-card.png".format(osu[0]["username"])
            card = discord.File(fp=BytesIO(await response.read()), filename=filename)
            embed.set_image(url=f"attachment://{filename}")
            embed.set_footer(
                text="Powered by api.martinebot.com", 
                icon_url="https://img.icons8.com/color/48/000000/osu.png"
            )
            await ctx.send(embed=embed, file=card)
        elif response.status in [404, 410, 422]:
            await ctx.send((await response.json())['message'])
        else:
            await ctx.send("API is currently down, please try again later.")