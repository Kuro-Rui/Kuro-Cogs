# Remove command logic originally from: https://github.com/mikeshardmind/SinbadCogs/tree/v3/messagebox

import asyncio
import datetime
import logging
import random
import time

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box

from .gifs import ping_pong_gifs

ping_gifs_picker = random.choice(ping_pong_gifs)

old_ping = None
log = logging.getLogger("red.kuro-cogs.botping")


class BotPing(commands.Cog):
    """A more information rich ping message."""

    __author__ = ["Kuro"]
    __version__ = "1.1.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Authors :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=325236743863625234572,
            force_registration=True,
        )
        default_global = {"use_gifs": True}
        self.config.register_global(**default_global)
        self.settings = {}

    async def initialize(self):
        self.settings = await self.config.all()

    async def red_delete_data_for_user(self, **kwargs):
        return

    def cog_unload(self):
        global old_ping
        if old_ping:
            try:
                self.bot.remove_command("ping")
            except:
                pass
            self.bot.add_command(old_ping)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.group(invoke_without_command=True)
    async def ping(self, ctx):
        """View bot latency."""
        start = time.monotonic()
        message = await ctx.send("Pinging...")
        end = time.monotonic()
        e = discord.Embed(title="Pinging...")
        overall = round((end - start) * 1000, 2)
        e.add_field(name="Overall Ping:", value=box(f"{overall}" + " ms", "py"))
        if await self.config.use_gifs():
            e.set_image(url=ping_gifs_picker)
        await asyncio.sleep(0.25)
        try:
            await message.edit(content=None, embed=e)
        except discord.NotFound:
            return

        latency = round(self.bot.latency * 1000, 2)
        e.add_field(name="Discord WebSocket:", value=box(f"{latency}" + " ms", "py"))
        await asyncio.sleep(0.25)
        try:
            await message.edit(embed=e)
        except discord.NotFound:
            return

        shards_ping = []
        shards_latency = []
        for shard_id, shard in self.bot.shards.items():
            latency = round(shard.latency * 1000, 2)
            shards_latency.append(latency)
            shards_ping.append(box(f"Shard {shard_id + 1}: {latency}" + " ms", "py"))
        e.add_field(name="Shards Ping:", value="\n".join(shards_ping))
        average = sum(shards_latency) / len(shards_latency)
        if average >= 1000:
            e.color = discord.Colour.red()
        elif average >= 200:
            e.color = discord.Colour.orange()
        else:
            e.color = discord.Colour.green()
        e.set_footer(text=f"Average: {round(average, 2)} ms")
        e.title = "Pong! 🏓"
        await asyncio.sleep(0.25)
        try:
            await message.edit(embed=e)
        except discord.NotFound:
            return

    @ping.command()
    async def message(self, ctx: commands.Context):
        """Show message latencies.

        This includes when message received, sent, and edited.
        """
        now = datetime.datetime.utcnow().timestamp()
        receive = round((now - ctx.message.created_at.timestamp()) * 1000, 2)

        e = discord.Embed(title="Pinging...")
        e.add_field(name="Message Receive:", value=box(f"{receive}" + " ms", "py"))

        send_start = time.monotonic()
        message = await ctx.send(embed=e)
        send_end = time.monotonic()
        send = round((send_end - send_start) * 1000, 2)
        e.add_field(name="Message Send:", value=box(f"{send}" + " ms", "py"))
        if await self.config.use_gifs():
            e.set_image(url=ping_gifs_picker)

        await asyncio.sleep(0.25)
        edit_start = time.monotonic()
        try:
            await message.edit(embed=e)
        except discord.NotFound:
            return
        edit_end = time.monotonic()
        edit = round((edit_end - edit_start) * 1000, 2)
        e.add_field(name="Message Edit:", value=box(f"{edit}" + " ms", "py"))

        average_ping = (receive + send + edit) / 3
        if average_ping >= 1000:
            e.color = discord.Colour.red()
        elif average_ping >= 200:
            e.color = discord.Colour.orange()
        else:
            e.color = discord.Colour.green()
        e.title = "Pong! 🏓"
        await asyncio.sleep(0.25)
        try:
            await message.edit(embed=e)
        except discord.NotFound:
            return

    @commands.is_owner()
    @commands.group()
    async def pingset(self, ctx: commands.Context):
        """Manage BotPing settings."""

    @pingset.command(name="usegifs", aliases=["usegif", "gif"])
    async def pingset_usegifs(self, ctx: commands.Context, true_or_false: bool = None):
        """Toggle displaying GIFs on the ping embed."""
        target_state = (
            true_or_false if true_or_false is not None else not (await self.config.use_gifs())
        )
        await self.config.use_gifs.set(target_state)
        self.settings["use_gifs"] = target_state
        word = "will" if target_state else "won't"
        await ctx.send(
            f"Ping Pong GIFs {word} be displayed on the `{ctx.clean_prefix}ping` embed."
        )


async def setup(bot):
    global old_ping
    old_ping = bot.get_command("ping")
    if old_ping:
        bot.remove_command(old_ping.name)

    cog = BotPing(bot)
    await cog.initialize()
    bot.add_cog(cog)
