import aiohttp
from io import BytesIO
from typing import Optional, Union

import discord
from redbot.core import commands, Config, checks

from .utils import osu_api_call, get_osu_avatar, send_osu_user_info

class Osu(commands.Cog):
    """Show osu! user stats with osu! API"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=842364413)
        self.config.register_global(ssh_emoji=None, ss_emoji=None, sh_emoji=None, s_emoji=None, a_emoji=None)
        self.config.register_user(username=None)
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

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
        ssh_emoji: Union[discord.Emoji, str], ss_emoji: Union[discord.Emoji, str],
        sh_emoji: Union[discord.Emoji, str], s_emoji: Union[discord.Emoji, str], a_emoji: Union[discord.Emoji, str]
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
    async def ssh(self, ctx, ssh_emoji: Optional[Union[discord.Emoji, str]]):
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
    async def ss(self, ctx, ss_emoji: Optional[Union[discord.Emoji, str]]):
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
    async def sh(self, ctx, sh_emoji: Optional[Union[discord.Emoji, str]]):
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
    async def s(self, ctx, s_emoji: Optional[Union[discord.Emoji, str]]):
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
    async def a(self, ctx, a_emoji: Optional[Union[discord.Emoji, str]]):
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

    @commands.command(aliases=["osuav"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def osuavatar(self, ctx, *, username: Optional[str]):
        """Shows your/another user osu! Avatar"""

        osu = await osu_api_call(self, ctx, username=username)
        avatar, avatar_url, filename = await get_osu_avatar(self, ctx, username)
        
        embed = discord.Embed(
            title="{}'s osu! Avatar".format(osu[0]["username"]), 
            url=avatar_url, 
            color=await ctx.embed_color()
        )
        embed.set_image(url=f"attachment://{filename}")
        await ctx.send(embed=embed, file=avatar)

    @commands.command(aliases=["osu", "std"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def standard(self, ctx, *, username: Optional[str]):
        """Shows an osu!standard User Stats!"""

        await send_osu_user_info(self, ctx, 0, username)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def taiko(self, ctx, *, username: Optional[str]):
        """Shows an osu!taiko User Stats!"""

        await send_osu_user_info(self, ctx, 1, username)

    @commands.command(aliases=["ctb", "catchthebeat"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def catch(self, ctx, *, username: Optional[str]):
        """Shows an osu!catch User Stats!"""

        await send_osu_user_info(self, ctx, 2, username)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def mania(self, ctx, *, username: Optional[str]):
        """Shows an osu!mania User Stats!"""

        await send_osu_user_info(self, ctx, 3, username)

    @commands.command(aliases=["osuc", "osuimage", "osuimg"])
    @commands.cooldown(60, 60, commands.BucketType.default)
    @commands.bot_has_permissions(embed_links=True)
    async def osucard(self, ctx, *, username: Optional[str]):
        """Shows an osu!standard User Card!""" # Thanks epic guy, thanks Preda <3

        osu = await osu_api_call(self, ctx, username=username)
        async with self.session.get(
            "https://api.martinebot.com/v1/imagesgen/osuprofile?player_username={}".format(osu[0]["username"])
        ) as resp:
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