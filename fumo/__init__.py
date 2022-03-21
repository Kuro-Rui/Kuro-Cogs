import aiohttp

from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list

from .utils import summon_fumo


class Fumo(commands.Cog):
    """
    Le Fumo Cog.
    """

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    __author__ = humanize_list(["Kuro"])
    __version__ = "1.1.3"

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
    
    @commands.group()
    async def fumo(self, ctx):
        """Generates Fumo Image."""
        pass

    @fumo.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def random(self, ctx):
        """Generates a random Fumo!"""
        
        await summon_fumo(self, ctx, "random")

    @fumo.command(aliases=["images"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def image(self, ctx):
        """Generates a random Fumo image."""
        
        await summon_fumo(self, ctx, "image")

    @fumo.command(aliases=["gifs"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def gif(self, ctx):
        """Generates a random Fumo GIF."""
        
        await summon_fumo(self, ctx, "gif")

    @fumo.command(aliases=["memes"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meme(self, ctx):
        """Generates a random Fumo meme."""
        
        await summon_fumo(self, ctx, "meme")

def setup(bot):
    bot.add_cog(Fumo(bot))

__red_end_user_data_statement__ = "This cog does not store any end user data."