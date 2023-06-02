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

from typing import Dict, Union

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import humanize_list

from .views import ChairsView, StartingView


class Chairs(commands.Cog):
    """Game of Chairs in Discord!"""

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.0.1"

    def __init__(self, bot: Red):
        self.bot = bot
        self.cache: Dict[int, Union[StartingView, ChairsView]] = {}
        self.config = Config.get_conf(self, identifier=754638472)
        self.config.register_guild(manager_role=None)

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    @commands.hybrid_group()
    async def chairs(self, ctx: commands.Context):
        """Play the game of Chairs!"""
        pass

    @chairs.command(name="start")
    async def chairs_start(self, ctx: commands.Context):
        """Start the game of Chairs!"""
        if not (manager_role := await self.config.guild(ctx.guild).manager_role()):
            await ctx.send("The manager role hasn't been set yet.")
            return
        manager_role = ctx.guild.get_role(manager_role)
        if manager_role not in ctx.author.roles:
            await ctx.send("You are not a manager.")
            return
        if self.cache.get(ctx.channel.id):
            await ctx.send("There is already a game of Chairs in this channel.")
            return
        view = StartingView()
        await view.start(ctx)

    @chairs.command(name="stop")
    async def chairs_stop(self, ctx: commands.Context):
        """Stop the game of Chairs."""
        if not (manager_role := await self.config.guild(ctx.guild).manager_role()):
            await ctx.send("The manager role hasn't been set yet.")
            return
        manager_role = ctx.guild.get_role(manager_role)
        if manager_role not in ctx.author.roles:
            await ctx.send("You are not a manager.")
            return
        if not (view := self.cache.get(ctx.channel.id)):
            await ctx.send("There is no game of Chairs in this channel.")
            return
        await view.stop_game(ctx.author)
        await ctx.send("The game has been cancelled successfully.")

    @commands.admin_or_permissions(manage_guild=True)
    @chairs.group(name="set", with_app_command=False)
    async def chairs_set(self, ctx: commands.Context):
        """Chairs game configuration."""
        pass

    @chairs_set.command(name="managerrole")
    async def chairs_set_managerrole(self, ctx: commands.Context, role: discord.Role = None):
        """Set the manager role. Omit role to reset."""
        if not role:
            await self.config.guild(ctx.guild).manager_role.clear()
            await ctx.send("The manager role has been reset.")
            return
        await self.config.guild(ctx.guild).manager_role.set(role.id)
        await ctx.send(f"The manager role has been set to {role.mention}.")
