from asyncio import sleep
from random import choice, randint
from string import ascii_letters

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list


def loading(step: int):
    l = ["▖", "▘", "▝", "▗"]
    screen = f"[{l[step]}]"
    return screen


class Hack(commands.Cog):
    """Le professional hecker."""

    def __init__(self, bot):
        self.bot = bot

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.guild_only()
    @commands.cooldown(1, 25, commands.BucketType.channel)
    @commands.command(aliases=["heck"])
    async def hack(self, ctx, member: discord.Member):
        """Hack someone!"""

        # Mass editing lol, must add handler on each :D
        message = await ctx.send(f"{loading(0)} Hacking {member.nick} now...")
        await sleep(2)
        try:
            await message.edit(content=f"{loading(1)} Finding Discord Login...")
        except discord.NotFound:
            return
        await sleep(2)
        try:
            await message.edit(content=f"{loading(2)} Bypassing 2FA...")
        except discord.NotFound:
            return
        await sleep(3)
        email = member.name.replace(" ", "_").replace("'", "") + "@gmail.com"
        password = "".join(choice(ascii_letters) for letters in range(10))
        try:
            await message.edit(
                content=(
                    f"{loading(3)} Found login information:\n"
                    f"**Email**: `{email}`\n"
                    f"**Password**: `{password}`"
                )
            )
        except discord.NotFound:
            return
        await sleep(4)
        try:
            await message.edit(content=f"{loading(0)} Fetching user DMs...")
        except discord.NotFound:
            return
        await sleep(1)
        last_dm = choice(
            [
                "man I love my mommy.",
                "can I see your feet pics?",
                "yeah I'm just built different.",
                "UwU",
                "pwetty pwease?",
                "dont frgt to like and subscrube!!",
                "I think it's smaller than most.",
                "I hope blueballs aren't real.",
                "yeah she goes to another school.",
                "imagine having a peen as small as mine in 2022",
                "I hope noone sees my nudes folder.",
                "honestly I'm pretty sure blue waffle is real and I have it.",
            ]
        )
        try:
            await message.edit(content=f"{loading(1)} **Last DM**: \"{last_dm}\"")
        except discord.NotFound:
            return
        await sleep(3)
        try:
            await message.edit(content=f"{loading(2)} Injecting trojan virus into {member}...")
        except discord.NotFound:
            return
        await sleep(2)
        try:
            await message.edit(content=f"{loading(3)} Virus injected. Finding IP Address...")
        except discord.NotFound:
            return
        await sleep(3)
        ip_address = f"{randint(50, 255)}.{randint(50, 255)}.{randint(50, 255)}.{randint(50, 255)}"
        try:
            await message.edit(content=f"{loading(0)} **IP Address**: `{ip_address}`")
        except discord.NotFound:
            return
        await sleep(2)
        try:
            await message.edit(content=f"{loading(1)} Selling user data to the government...")
        except discord.NotFound:
            return
        await sleep(2)
        try:
            await message.edit(content=f"{loading(2)} Reporting account to Discord for breaking ToS...")
        except discord.NotFound:
            return
        await sleep(1)
        try:
            await message.edit(content=f"{commands.context.TICK} Finished hacking {member.nick}.")
        except discord.NotFound:
            return
        await ctx.send("The *totally* real and dangerous hack is complete.")
