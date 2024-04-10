"""
MIT License

Copyright (c) 2020-present phenom4n4n

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

from typing import Optional, Set

import discord
import kuroutils
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import box


class PermissionsLocker(kuroutils.Cog):
    """Force permissions for the bot."""

    __author__ = ["PhenoM4n4n", "Kuro"]
    __version__ = "1.3.2"

    def __init__(self, bot: Red) -> None:
        super().__init__(bot)
        self._config = Config.get_conf(
            self, identifier=4235969345783789456, force_registration=True
        )
        default_global = {"permissions": 0, "whitelisted": []}
        self._config.register_global(**default_global)

        self.perms: Optional[discord.Permissions] = None
        self.whitelist: Set[int] = set()

    async def cog_load(self):
        await super().cog_load()
        data = await self._config.all()
        self.perms = discord.Permissions(data["permissions"])
        self.whitelist.update(data["whitelisted"])
        self.bot.before_invoke(self.before_invoke_hook)

    async def cog_unload(self):
        super().cog_unload()
        self.bot.remove_before_invoke_hook(self.before_invoke_hook)
        async with self._config.whitelisted() as whitelist:
            whitelist.clear()
            whitelist.extend(self.whitelist)

    # Original invoke hook logic from
    # https://github.com/mikeshardmind/SinbadCogs/blob/v3/noadmin/__init__.py#L14-L38
    async def before_invoke_hook(self, ctx: commands.Context):
        if not ctx.guild or isinstance(ctx.command, commands.commands._AlwaysAvailableCommand):
            return
        if ctx.guild.id in self.whitelist:
            return
        me = ctx.guild.me
        if me == ctx.guild.owner:
            return
        if await ctx.bot.is_owner(ctx.author):
            return

        required_perms = self.perms
        my_perms = ctx.channel.permissions_for(me)
        if not my_perms.is_superset(required_perms):
            missing_perms = self.humanize_perms(
                discord.Permissions(
                    (my_perms.value ^ required_perms.value) & required_perms.value
                ),
                True,
            )
            await ctx.send(
                "Hello there!\nI'm missing the following permissions. "
                "Without these permissions, I cannot function properly.\n"
                "Please check your guild and channel permissions to ensure I have these permissions:\n"
                f"{box(missing_perms, 'diff')}",
                delete_after=60,
            )
            raise commands.CheckFailure()

    def humanize_perms(self, permissions: discord.Permissions, check: bool):
        perms = dict(permissions)
        perms_list = [f"+ {key}" for key, value in perms.items() if value == check]
        return "\n".join(perms_list)

    @commands.is_owner()
    @commands.group()
    async def permlock(self, ctx: commands.Context):
        """Permissions locker group command."""
        pass

    @permlock.command()
    async def perms(self, ctx: commands.Context, value: int):
        """Set the permissions value that is required for the bot to work."""
        permissions = discord.Permissions(value)
        await self._config.permissions.set(permissions.value)
        if value:
            await ctx.send(
                "I will now require these permissions on commands:\n"
                f"{box(self.humanize_perms(permissions, True), 'diff')}"
            )
        else:
            await ctx.send("Permissions requirement has been disabled.")
        self.perms = permissions

    @permlock.command(aliases=["wl"])
    async def whitelist(self, ctx, guild_id: int):
        """Whitelist a guild from PermissionsLocker checks."""
        async with self._config.whitelisted() as whitelist:
            if guild_id in whitelist:
                await ctx.send("This guild is already whitelisted!")
                return
            whitelist.append(guild_id)
        self.whitelist.add(guild_id)
        await ctx.tick()

    @permlock.command(aliases=["unwl"])
    async def unwhitelist(self, ctx, guild_id: int):
        """Remove a guild from the PermissionsLocker whitelist."""
        async with self._config.whitelisted() as whitelist:
            if guild_id not in whitelist:
                await ctx.send("This is not a guild in the whitelist!")
                return
            whitelist.remove(guild_id)
        self.whitelist.remove(guild_id)
        await ctx.tick()

    @commands.bot_has_permissions(embed_links=True)
    @permlock.command()
    async def settings(self, ctx: commands.Context):
        """View PermissionsLocker settings."""
        data = await self._config.all()
        embed = discord.Embed(color=await ctx.embed_color(), title="PermissionsLocker")
        embed.add_field(
            name="Required Permissions",
            value=str(data["permissions"])
            + box(
                self.humanize_perms(discord.Permissions(data["permissions"]), True),
                "diff",
            ),
            inline=False,
        )
        if data["whitelisted"]:
            whitelisted = [str(item) for item in data["whitelisted"]]
            embed.add_field(name="Whitelisted", value=", ".join(whitelisted), inline=False)
        await ctx.send(embed=embed)
