from __future__ import annotations

import logging
from logging import basicConfig, DEBUG
import random

import discord
from discord.ext import tasks
from discord_ui import View
import dislash
from dislash import *
from dislash.interactions import ActionRow, Button, ButtonStyle
from dislash.interactions.application_command import *

# from redbot.core import bot
from redbot.core import commands
# from redbot.core.i18n import cog_i18n, Translator
from redbot.core.utils.chat_formatting import humanize_list, humanize_number

log = logging.getLogger("red.slash.commands")

# _ = Translator("slash", __file__)


# @cog_i18n(_)
class SlashCommands(commands. Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_presence. start()

    def cog_unload(self):
        self.change_presence. cancel()

    bot_name = "Kiki✨"

    @slash_command(description=f"Vote for {bot_name}!")
    async def vote(self, inter):
        c = await self.bot.get_embed_colour(await ctx.embed_color())
        t = "Please Vote for Me!"
        d = "You can vote for me by clicking on the links below:"
        f = "Thanks for your support!"
        i = self.bot.user.avatar_url
        
        dot = "<a:Dot:914352680627994634>"

        topgg_link = "https://top.gg/bot/886547720985264178/vote"
        dbl_link = "https://discordbotlist.com/bots/kiki/upvote"
        milrato_link = "https://milrato-botlist.eu/bot/886547720985264178/vote"
        # No links for https://discords.com because I haven't submitted the bot there yet.
        discords_link = ""

        e = discord.Embed(title = t, description=d, colour = c)
        e.add_field(name="Links:", value=f"{dot}[`Top.gg`]({topgg_link})\n{dot}[`Discord Bot List`]({dbl_link})\n{dot}[`Milrato Bot List`]({milrato_link})")
        e.set_thumbnail(url=i)
        e.set_footer(text=f)

        vote_button = [
            ActionRow(
                Button(
                    style=ButtonStyle.link,
                    label="Top.gg",
                    emoji=discord.PartialEmoji(name="topgg", animated=False, id="918280202398875758"),
                    url=topgg_link
                ),
                Button(
                    style=ButtonStyle.link,
                    label="discordbotlist.com",
                    emoji=discord.PartialEmoji(name="dbl", animated=False, id="757235965629825084"),
                    url=dbl_link
                ),
                Button(
                    style=ButtonStyle.link,
                    label="milrato-botlist.eu",
                    emoji=discord.PartialEmoji(name="OLD_Milrato", animated=False, id="840259659163893820"),
                    url=milrato_link
                )
            )
        ]
        await inter.reply(embed=e, components=vote_button)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        guild = self.bot.get_guild(825535079719501824)
        channel = guild.get_channel(908718864790077532)
        await channel. send(
            f"Traceback:\n{__import__('traceback').format_exc()}\n{error}"
        )
        view = View()
        view.add_item(
            discord.ui.Button(
                label="ʚ﹕The Cloud House﹕ɞ",
                url="https://discord.gg/Zef3pD8Yt5",
                emoji=discord.PartialEmoji(name="SleepingZzZ", animated=True, id="915569880160436264"),
            )
        )
        bot_name = "Kiki✨"
            
        if isinstance(error, commands.MissingPermissions):
            await inter. send("You can't use this command.", hidden=True, view=View())

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await inter. send(
                    "You can't use this command in DMs.",
                    hidden=True,
                    view=View(),
                )
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BotMissingPermissions):
            await inter.send(
                f"Sorry, {bot_name} doesn't have permissions to execute this command.",
                hidden=True,
                view=View(),
            )

        elif isinstance(error, commands.CommandInvokeError):
            await inter.send(
                f"Sorry, {bot_name} doesn't have permissions to execute this command.",
                hidden=True,
                view=View(),
            )

        else:
            pass


def setup(bot):
    bot.add_cog(SlashCommands(bot))