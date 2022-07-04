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

# Remove command logic originally from: https://github.com/mikeshardmind/SinbadCogs/tree/v3/messagebox

import asyncio
import datetime
import random
import time

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box, humanize_list

old_ping = None
ping_pong_gifs = [
    "https://i.pinimg.com/originals/ac/b8/8f/acb88f71e5ed54072a24f647e28a9c3f.gif",
    "https://4.bp.blogspot.com/-8XanbCQDxfg/WnJTaUeifYI/AAAAAAABEUo/5yv_KUlLV9cmJsuI8jeFRrGSXbtQMclngCKgBGAs/s1600/Omake%2BGif%2BAnime%2B-%2BShokugeki%2Bno%2BSoma%2BS2%2B-%2BOAD%2B1%2B%255BDVD%255D%2B-%2BMegumi%2Bvs%2BIsshiki.gif",
    "https://remyfool.files.wordpress.com/2016/11/agari-rally.gif?w=924",
    "https://i.imgur.com/LkdjWE6.gif",
    "https://i.gifer.com/6TaL.gif",
    "https://i.kym-cdn.com/photos/images/original/000/753/601/bc8.gif",
    "https://c.tenor.com/On7v3wlDxNUAAAAd/ping-pong-anime.gif",
    "https://imgur.com/1cnscjV.gif",
    "https://images.squarespace-cdn.com/content/v1/5b23e822f79392038cbd486c/1589129513917-X6QBWRXBHLCSFXT9INR2/b17c1b31e185d12aeca55b576c1ecaef.gif",
    "https://i1.wp.com/drunkenanimeblog.com/wp-content/uploads/2017/11/shakunetsu-no-takkyuu-musume-scorching-ping-pong-girls.gif?fit=540%2C303&ssl=1&resize=350%2C200https://media1.tenor.com/images/2b27c6e7747d319f76fd98d2a226ab33/tenor.gif?itemid=15479836",
]


class BotPing(commands.Cog):
    """Detailed bot latency information."""

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.1.0"

    def format_help_for_context(self, ctx: commands.Context):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Authors :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

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
        """View [botname]'s latency."""
        start = time.monotonic()
        message = await ctx.send("Pinging...")
        end = time.monotonic()
        e = discord.Embed(title="Pinging...")
        overall = round((end - start) * 1000, 2)
        e.add_field(name="Overall Ping:", value=box(f"{overall}" + " ms", "py"))
        if await self.config.use_gifs():
            e.set_image(url=random.choice(ping_pong_gifs))
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

        if self.bot.shard_count > 1:
            shards_ping = []
            shards_latency = []
            for shard_id, shard in self.bot.shards.items():
                latency = round(shard.latency * 1000, 2)
                shards_latency.append(latency)
                shards_ping.append(box(f"Shard {shard_id + 1}: {latency}" + " ms", "py"))
            e.add_field(name="Shards Ping:", value="\n".join(shards_ping), inline=False)
            average = sum(shards_latency) / len(shards_latency)
        else:
            average = (overall + latency) / 2
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
        """
        Show message latencies.

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
            e.set_image(url=random.choice(ping_pong_gifs))

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
        pass

    @pingset.command(name="usegifs", aliases=["usegif", "gif"])
    async def pingset_usegifs(self, ctx: commands.Context, true_or_false: bool = None):
        """Toggle displaying GIFs on the ping embed."""
        target_state = (
            true_or_false if true_or_false is not None else not (await self.config.use_gifs())
        )
        await self.config.use_gifs.set(target_state)
        self.settings["use_gifs"] = target_state
        word = "will" if target_state else "won't"
        await ctx.send(f"Ping Pong GIFs {word} be displayed on the `{ctx.prefix}ping` embed.")


async def setup(bot):
    global old_ping
    old_ping = bot.get_command("ping")
    if old_ping:
        bot.remove_command(old_ping.name)

    cog = BotPing(bot)
    await cog.initialize()
    bot.add_cog(cog)
