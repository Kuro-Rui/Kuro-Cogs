import aiohttp
from io import BytesIO
from typing import Optional

import discord
from redbot.core import commands, Config, checks
from redbot.core.utils.chat_formatting import humanize_number, humanize_timedelta


class Osu(commands.Cog):
    """Show osu! user stats with osu! API"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=842364413)
        self.config.register_global(apikey=None, ssh_emoji=None, ss_emoji=None, sh_emoji=None, s_emoji=None, a_emoji=None)
        self.config.register_user(username=None)

    @commands.group()
    async def osuset(self, ctx):
        """Settings for osu!"""
        pass

    @osuset.command(aliases=["key"])
    @checks.is_owner()
    async def apikey(self, ctx, api_key: str = None):
        """Set osu! API key"""
        if not api_key:
            await self.config.apikey.clear()
            await ctx.tick()
            await ctx.send("The API key has been removed.")
        else:
            headers = {"content-type": "application/json", "user-key": api_key}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://osu.ppy.sh/api/get_user?k={api_key}&u=peppy", headers=headers) as response:
                    osu = await response.json()
            if response.status == 200:
                await self.config.apikey.set(api_key)
                await ctx.message.delete() # Delete the message for safety
                await ctx.send("The API key has been set.")
            else:
                await ctx.send(osu["error"])

    @osuset.command(aliases=["name"])
    async def username(self, ctx, *, username: str = None):
        """Set your osu! username."""

        apikey = await self.config.apikey()
        headers = {"content-type": "application/json", "user-key": apikey}

        if apikey == None:
            await ctx.send("The API Key hasn't been set yet!")
            return
        else:
            if username == None:
                await self.config.user(ctx.author).username.clear()
                await ctx.tick()
                await ctx.send("Your username has been removed.")
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.post(f"https://osu.ppy.sh/api/get_user?k={apikey}&u={username}", headers=headers) as response:
                        osu = await response.json()
                if osu:
                    await self.config.user(ctx.author).username.set(username)
                    await ctx.tick()
                    await ctx.send(f"Your username has been set to `{username}`.")
                else:
                    await ctx.send(f"I can't find any player with the name `{username}`.")
    
    @osuset.group()
    @checks.is_owner()
    async def emoji(self, ctx):
        """Set custom emoji for ranks."""
        pass

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def ssh(self, ctx, ssh_emoji: Optional[discord.Emoji]):
        """Set custom emoji for SSH rank."""
        if not ssh_emoji:
            await self.config.ssh_emoji.clear()
            await ctx.send("Custom emoji for SSH Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(ssh_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            await self.config.ssh_emoji.set(ssh_emoji.id)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def ss(self, ctx, ss_emoji: Optional[discord.Emoji]):
        """Set custom emoji for SS rank."""
        if not ss_emoji:
            await self.config.ss_emoji.clear()
            await ctx.send("Custom emoji for SS Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(ss_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            await self.config.ss_emoji.set(ss_emoji.id)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def sh(self, ctx, sh_emoji: Optional[discord.Emoji]):
        """Set custom emoji for SH rank."""
        if not sh_emoji:
            await self.config.sh_emoji.clear()
            await ctx.send("Custom emoji for SH Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(sh_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            await self.config.sh_emoji.set(sh_emoji.id)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def s(self, ctx, s_emoji: Optional[discord.Emoji]):
        """Set custom emoji for S rank."""
        if not s_emoji:
            await self.config.s_emoji.clear()
            await ctx.send("Custom emoji for S Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(s_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            await self.config.s_emoji.set(s_emoji.id)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def a(self, ctx, a_emoji: Optional[discord.Emoji]):
        """Set custom emoji for A rank."""
        if not a_emoji:
            await self.config.a_emoji.clear()
            await ctx.send("Custom emoji for A Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(a_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            await self.config.a_emoji.set(a_emoji.id)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    async def clear(self, ctx):
        """Clear all set custom emojis for ranks."""
        await self.config.ssh_emoji.clear()
        await self.config.ss_emoji.clear()
        await self.config.sh_emoji.clear()
        await self.config.s_emoji.clear()
        await self.config.a_emoji.clear()
        await ctx.tick()
        await ctx.send("All custom emojis for ranks has been cleared.")

    @commands.command(aliases=["osu", "std"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def standard(self, ctx, *, username: str = None):
        """Shows an osu!standard User Stats!"""

        if username == None:
            username = await self.config.user(ctx.author).username()
            if username == None:
                p = ctx.clean_prefix
                command = self.bot.get_command("std").name
                error = (
                    f"Your username hasn't been set yet. You can set it with `{p}osuset username <username>`\n"
                    f"You can also provide a username in this command: `{p}{command} <username>`"
                )
                await ctx.send(error)
                return

        await self.send_user_info(ctx, 0, username)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def taiko(self, ctx, *, username: str = None):
        """Shows an osu!taiko User Stats!"""

        if username == None:
            username = await self.config.user(ctx.author).username()
            if username == None:
                p = ctx.clean_prefix
                command = self.bot.get_command("std").name
                error = (
                    f"Your username hasn't been set yet. You can set it with `{p}osuset username <username>`\n"
                    f"You can also provide a username in this command: `{p}{command} <username>`"
                )
                await ctx.send(error)
                return

        await self.send_user_info(ctx, 1, username)

    @commands.command(aliases=["ctb", "catchthebeat"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def catch(self, ctx, *, username: str = None):
        """Shows an osu!catch User Stats!"""

        if username == None:
            username = await self.config.user(ctx.author).username()
            if username == None:
                p = ctx.clean_prefix
                command = self.bot.get_command("std").name
                error = (
                    f"Your username hasn't been set yet. You can set it with `{p}osuset username <username>`\n"
                    f"You can also provide a username in this command: `{p}{command} <username>`"
                )
                await ctx.send(error)
                return

        await self.send_user_info(ctx, 2, username)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def mania(self, ctx, *, username: str = None):
        """Shows an osu!mania User Stats!"""

        if username == None:
            username = await self.config.user(ctx.author).username()
            if username == None:
                p = ctx.clean_prefix
                command = self.bot.get_command("std").name
                error = (
                    f"Your username hasn't been set yet. You can set it with `{p}osuset username <username>`\n"
                    f"You can also provide a username in this command: `{p}{command} <username>`"
                )
                await ctx.send(error)
                return

        await self.send_user_info(ctx, 3, username)

    @commands.command(aliases=["osuc", "osuimage", "osuimg"])
    @commands.cooldown(60, 60, commands.BucketType.default)
    @commands.bot_has_permissions(embed_links=True)
    async def osucard(self, ctx, *, username: str = None):
        """Shows an osu!standard User Card!""" # Thanks epic guy, thanks Preda <3

        apikey = await self.config.apikey()
        headers = {"content-type": "application/json", "user-key": apikey}

        if apikey is None:
            await ctx.send("The API Key hasn't been set yet!")
            return

        if username is None:
            username = await self.config.user(ctx.author).username()
            if username is None:
                p = ctx.clean_prefix
                command = self.bot.get_command("osucard").name
                error = (
                    f"Your username hasn't been set yet. You can set it with `{p}osuset username <username>`\n"
                    f"You can also provide a username in this command: `{p}{command} <username>`"
                )
                await ctx.send(error)
                return

        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.post(f"https://osu.ppy.sh/api/get_user?k={apikey}&u={username}", headers=headers) as response:
                    osu = await response.json()
                async with s.get(f"https://api.martinebot.com/v1/imagesgen/osuprofile?&player_username={username}") as resp:
                    if resp.status in (200,201):
                        embed = discord.Embed(title="{}'s osu! Standard Stats:".format(osu[0]["username"]), url="https://osu.ppy.sh/users/{}".format(osu[0]["user_id"]), colour=await ctx.embed_colour())
                        file = discord.File(fp=BytesIO(await resp.read()), filename=f"osu_profile.png")
                        embed.set_image(url="attachment://osu_profile.png")
                        osu_icon = "https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png"
                        embed.set_footer(text="Powered by api.martinebot.com", icon_url=osu_icon)
                        await ctx.send(embed=embed, file=file)
                        file.close()
                    elif resp.status in (404,410,422):
                        await ctx.send((await resp.json())['message'])
                    else:
                        await ctx.send("API is currently down, please try again later.")

    async def send_user_info(self, ctx, m: int, username: str = None):
        """osu! User Info Embed"""
        
        apikey = await self.config.apikey()

        if apikey is None:
            await ctx.send("The API Key hasn't been set yet!")
            return

        if m == 0:
            mode = "Standard"
            icon = "https://icon-library.com/images/osu-icon/osu-icon-16.jpg"
        elif m == 1:
            mode = "Taiko"
            icon = "https://lemmmy.pw/osusig/img/taiko.png"
        elif m == 2:
            mode = "Catch"
            icon = "https://www.seekpng.com/png/full/194-1941038_osu-ctb-back-white-icon-png.png"
        else:
            mode = "Mania"
            icon = "https://icon-library.com/images/osu-icon/osu-icon-15.jpg"

        headers = {"content-type": "application/json", "user-key": apikey}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://osu.ppy.sh/api/get_user?k={apikey}&u={username}&m={m}", headers=headers) as response:
                osu = await response.json()
            async with session.get("https://a.ppy.sh/{}".format(osu[0]["user_id"])) as resp:
                file = discord.File(fp=BytesIO(await resp.read()), filename=f"osu_avatar.png")

        if osu:
            ssh_emoji, ss_emoji, sh_emoji, s_emoji, a_emoji = await self.rank_emojis(ctx)
            # Inspired by owo#0498 (Thanks Stevy 😹)
            description = (
                "**▸ Joined at:** {}\n"
                "**▸ Rank:** #{} (:flag_{}: #{})\n"
                "**▸ Level:** {}\n"
                "**▸ PP:** {}\n"
                "**▸ Accuracy:** {} %\n"
                "**▸ Playcount:** {}\n"
                "**▸ Playtime:** {}\n"
                "**▸ Ranks:** {}`{}` {}`{}` {}`{}` {}`{}` {}`{}`\n"
                "**▸ Ranked Score:** {}\n"
                "**▸ Total Score:** {}"
            ).format(
                osu[0]["join_date"][:10], 
                humanize_number(osu[0]["pp_rank"]), osu[0]["country"].lower(), humanize_number(osu[0]["pp_country_rank"]), 
                osu[0]["level"][:5], osu[0]["pp_raw"], osu[0]["accuracy"][:6],
                humanize_number(osu[0]["playcount"]), humanize_timedelta(seconds=osu[0]["total_seconds_played"]),
                ssh_emoji, osu[0]["count_rank_ssh"], ss_emoji, osu[0]["count_rank_ss"], 
                sh_emoji, osu[0]["count_rank_sh"], s_emoji, osu[0]["count_rank_s"], a_emoji, osu[0]["count_rank_a"],
                humanize_number(osu[0]["ranked_score"]), humanize_number(osu[0]["total_score"])
            )

            embed = discord.Embed(description=description, color=await ctx.embed_color())
            embed.set_author(
                icon_url=icon,
                url="https://osu.ppy.sh/u/{}".format(osu[0]["user_id"]),
                name="osu! {} Profile for {}".format(mode, osu[0]["username"])
            )
            embed.set_footer(text="Powered by osu!", icon_url="https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png")
            embed.set_thumbnail(url="attachment://osu_avatar.png")
            await ctx.send(embed=embed, file=file)
            file.close()
        else:
            await ctx.send("No results found for this player.")

    async def rank_emojis(self, ctx):
        ssh_emoji = self.bot.get_emoji(await self.config.ssh_emoji())
        if not ssh_emoji:
            ssh_emoji = "**SSH** "
        ss_emoji = self.bot.get_emoji(await self.config.ss_emoji())
        if not ss_emoji:
            ss_emoji = "**SS** "
        sh_emoji = self.bot.get_emoji(await self.config.sh_emoji())
        if not sh_emoji:
            sh_emoji = "**SH** "
        s_emoji = self.bot.get_emoji(await self.config.s_emoji())
        if not s_emoji:
            s_emoji = "**S** "
        a_emoji = self.bot.get_emoji(await self.config.a_emoji())
        if not a_emoji:
            a_emoji = "**A** "
        return ssh_emoji, ss_emoji, sh_emoji, s_emoji, a_emoji