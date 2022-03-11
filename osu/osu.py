import aiohttp
from io import BytesIO
from typing import Union

import discord
from redbot.core import commands, Config, checks
from redbot.core.utils.chat_formatting import humanize_number, humanize_timedelta

class Osu(commands.Cog):
    """Show osu! user stats with osu! API"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=842364413)
        self.config.register_global(ssh_emoji=None, ss_emoji=None, sh_emoji=None, s_emoji=None, a_emoji=None)
        self.config.register_user(username=None)
        self.session = aiohttp.ClientSession()

    @commands.group()
    async def osuset(self, ctx):
        """Settings for osu!"""
        pass

    @osuset.command()
    @checks.is_owner()
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

    @osuset.command(aliases=["name"])
    async def username(self, ctx, *, username: str = None):
        """Set your osu! username."""

        api_key = (await self.bot.get_shared_api_tokens("osu")).get("api_key")
        headers = {"content-type": "application/json", "user-key": api_key}

        if not api_key:
            return await ctx.send("The API Key hasn't been set yet!")
        else:
            if not username:
                await self.config.user(ctx.author).username.clear()
                await ctx.tick()
                await ctx.send("Your username has been removed.")
            else:
                async with self.session.post(f"https://osu.ppy.sh/api/get_user?k={api_key}&u={username}", headers=headers) as response:
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
    async def multi(
        self, ctx,
        ssh_emoji: Union[discord.Emoji, discord.PartialEmoji, str],
        ss_emoji: Union[discord.Emoji, discord.PartialEmoji, str],
        sh_emoji: Union[discord.Emoji, discord.PartialEmoji, str],
        s_emoji: Union[discord.Emoji, discord.PartialEmoji, str],
        a_emoji: Union[discord.Emoji, discord.PartialEmoji, str]
    ):
        """Set custom emoji for all ranks at once!"""
        try:
            await ctx.message.add_reaction(ssh_emoji)
            await ctx.message.add_reaction(ss_emoji)
            await ctx.message.add_reaction(sh_emoji)
            await ctx.message.add_reaction(s_emoji)
            await ctx.message.add_reaction(a_emoji)
        except discord.HTTPException:
            return await ctx.send("Uh oh, I cannot use that emoji.")

        try:
            await self.config.ssh_emoji.set(ssh_emoji.id)
        except AttributeError: # Handle Original Emoji
            await self.config.ssh_emoji.set(ssh_emoji)
        
        try:
            await self.config.ss_emoji.set(ss_emoji.id)
        except AttributeError: # Handle Original Emoji
            await self.config.ss_emoji.set(ss_emoji)
        
        try:
            await self.config.sh_emoji.set(sh_emoji.id)
        except AttributeError: # Handle Original Emoji
            await self.config.sh_emoji.set(sh_emoji)
        
        try:
            await self.config.s_emoji.set(s_emoji.id)
        except AttributeError: # Handle Original Emoji
            await self.config.s_emoji.set(s_emoji)
        
        try:
            await self.config.a_emoji.set(a_emoji.id)
        except AttributeError: # Handle Original Emoji
            await self.config.a_emoji.set(a_emoji)
        
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def ssh(self, ctx, ssh_emoji: Union[discord.Emoji, str] = None):
        """Set custom emoji for SSH rank."""
        if not ssh_emoji:
            await self.config.ssh_emoji.clear()
            await ctx.send("Custom emoji for SSH Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(ssh_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")

            try:
                await self.config.ssh_emoji.set(ssh_emoji.id)
            except AttributeError: # Handle Original Emoji
                await self.config.ssh_emoji.set(ssh_emoji)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def ss(self, ctx, ss_emoji: Union[discord.Emoji, str] = None):
        """Set custom emoji for SS rank."""
        if not ss_emoji:
            await self.config.ss_emoji.clear()
            await ctx.send("Custom emoji for SS Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(ss_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            
            try:
                await self.config.ss_emoji.set(ss_emoji.id)
            except AttributeError: # Handle Original Emoji
                await self.config.ss_emoji.set(ss_emoji)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def sh(self, ctx, sh_emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None):
        """Set custom emoji for SH rank."""
        if not sh_emoji:
            await self.config.sh_emoji.clear()
            await ctx.send("Custom emoji for SH Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(sh_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            
            try:
                await self.config.sh_emoji.set(sh_emoji.id)
            except AttributeError: # Handle Original Emoji
                await self.config.sh_emoji.set(sh_emoji)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def s(self, ctx, s_emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None):
        """Set custom emoji for S rank."""
        if not s_emoji:
            await self.config.s_emoji.clear()
            await ctx.send("Custom emoji for S Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(s_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            
            try:
                await self.config.s_emoji.set(s_emoji.id)
            except AttributeError: # Handle Original Emoji
                await self.config.s_emoji.set(s_emoji)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    @commands.bot_has_permissions(add_reactions=True, use_external_emojis=True)
    async def a(self, ctx, a_emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None):
        """Set custom emoji for A rank."""
        if not a_emoji:
            await self.config.a_emoji.clear()
            await ctx.send("Custom emoji for A Rank removed.")
        else:
            try:
                await ctx.message.add_reaction(a_emoji)
            except discord.HTTPException:
                return await ctx.send("Uh oh, I cannot use that emoji.")
            
            try:
                await self.config.a_emoji.set(a_emoji.id)
            except AttributeError: # Handle Original Emoji
                await self.config.a_emoji.set(a_emoji)
        await ctx.tick()

    @emoji.command()
    @checks.is_owner()
    async def clear(self, ctx):
        """Clear all set custom emojis for ranks."""
        await self.config.clear()
        await ctx.tick()
        await ctx.send("All custom emojis for ranks has been cleared.")

    async def rank_emojis(self, ctx):
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

    @commands.command(aliases=["osu", "std"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def standard(self, ctx, *, username: str = None):
        """Shows an osu!standard User Stats!"""

        await self.send_osu_user_info(ctx, 0, username)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def taiko(self, ctx, *, username: str = None):
        """Shows an osu!taiko User Stats!"""

        await self.send_osu_user_info(ctx, 1, username)

    @commands.command(aliases=["ctb", "catchthebeat"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def catch(self, ctx, *, username: str = None):
        """Shows an osu!catch User Stats!"""

        await self.send_osu_user_info(ctx, 2, username)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def mania(self, ctx, *, username: str = None):
        """Shows an osu!mania User Stats!"""

        await self.send_osu_user_info(ctx, 3, username)

    @commands.command(aliases=["osuc", "osuimage", "osuimg"])
    @commands.cooldown(60, 60, commands.BucketType.default)
    @commands.bot_has_permissions(embed_links=True)
    async def osucard(self, ctx, *, username: str = None):
        """Shows an osu!standard User Card!""" # Thanks epic guy, thanks Preda <3

        api_key = (await self.bot.get_shared_api_tokens("osu")).get("api_key")
        headers = {"content-type": "application/json", "user-key": api_key}

        if api_key is None:
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
            async with self.session.post(f"https://osu.ppy.sh/api/get_user?k={api_key}&u={username}", headers=headers) as response:
                osu = await response.json()
            async with self.session.get(f"https://api.martinebot.com/v1/imagesgen/osuprofile?&player_username={username}") as resp:
                if resp.status in [200, 201]:
                    embed = discord.Embed(title="{}'s osu! Standard Stats:".format(osu[0]["username"]), url="https://osu.ppy.sh/users/{}".format(osu[0]["user_id"]), colour=await ctx.embed_colour())
                    file = discord.File(fp=BytesIO(await resp.read()), filename=f"osu_profile.png")
                    embed.set_image(url="attachment://osu_profile.png")
                    embed.set_footer(text="Powered by api.martinebot.com", icon_url="https://img.icons8.com/color/48/000000/osu.png")
                    await ctx.send(embed=embed, file=file)
                    file.close()
                elif resp.status in [404, 410, 422]:
                    await ctx.send((await resp.json())['message'])
                else:
                    await ctx.send("API is currently down, please try again later.")

    async def send_osu_user_info(self, ctx, m: int, username: str = None):
        """osu! User Info Embed"""
        
        api_key = (await self.bot.get_shared_api_tokens("osu")).get("api_key")

        if not api_key:
            error_msg = "The Owner hasn't set the API Key yet! "
            if ctx.author.id in self.bot.owner_ids:
                error_msg += "Set it with `{p}set api osu api_key <API_Key>`."
            return await ctx.send("The API Key hasn't been set yet!")

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

        headers = {"content-type": "application/json", "user-key": api_key}
        
        async with self.session.post(f"https://osu.ppy.sh/api/get_user?k={api_key}&u={username}&m={m}", headers=headers) as response:
            osu = await response.json()
        async with self.session.get("https://a.ppy.sh/{}".format(osu[0]["user_id"])) as image:
            file = discord.File(fp=BytesIO(await image.read()), filename=f"osu_avatar.png")

        if osu:
            ssh, ss, sh, s, a = await self.rank_emojis(ctx)
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
                osu[0]["level"][:5],
                osu[0]["pp_raw"],
                osu[0]["accuracy"][:6],
                humanize_number(osu[0]["playcount"]),
                humanize_timedelta(seconds=osu[0]["total_seconds_played"]),
                ssh, osu[0]["count_rank_ssh"], ss, osu[0]["count_rank_ss"], 
                sh, osu[0]["count_rank_sh"], s, osu[0]["count_rank_s"], a, osu[0]["count_rank_a"],
                humanize_number(osu[0]["ranked_score"]),
                humanize_number(osu[0]["total_score"])
            )

            embed = discord.Embed(description=description, color=await ctx.embed_color())
            embed.set_author(
                icon_url="https://lemmmy.pw/osusig/img/{}.png".format(icon),
                url="https://osu.ppy.sh/users/{}/{}".format(osu[0]["user_id"], type),
                name="osu! {} Profile for {}".format(mode, osu[0]["username"])
            )
            embed.set_footer(text="Powered by osu!", icon_url="https://img.icons8.com/color/48/000000/osu.png")
            embed.set_thumbnail(url="attachment://osu_avatar.png")
            await ctx.send(embed=embed, file=file)
            file.close()
        else:
            await ctx.send("No results found for this player.")