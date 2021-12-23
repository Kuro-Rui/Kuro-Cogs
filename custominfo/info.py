import discord

import dislash
from dislash.interactions import ActionRow, Button, ButtonStyle

from redbot.core import commands, checks, Config

old_info = None

class CustomInfo(commands.Cog):
    """Personalize Info command with an embed and buttons."""

    __author__ = "Kuro"

    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return

    def __init__(self, bot):
        self.bot = bot
        default = {
            "support": False,
            "support_serv": None,
            "setpermissions": "",
        }
        self.config = Config.get_conf(self, 376564057517457408, force_registration=True)
        self.config.register_global(**default)

    def cog_unload(self):
        global old_info
        if old_info:
            try:
                self.bot.remove_command("info")
            except:
                pass
            self.bot.add_command(old_info)
    
    @checks.is_owner()
    @commands.group()
    async def infoset(self, ctx):
        """Settings for CustomInfo cog."""
        pass

def setup(bot):
    info = CustomInfo(bot)
    global old_info
    old_info = bot.get_command("info")
    if old_info:
        bot.remove_command(old_info.name)
    bot.add_cog(info)