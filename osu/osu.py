import discord
from redbot.core import commands, Config, checks
from io import BytesIO
import aiohttp
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import humanize_number, humanize_timedelta

BaseCog = getattr(commands, "Cog", object)

class Osu(BaseCog):
    """Show stuff using osu!"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=842364413)
        default_global = {"apikey": ""}
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def osu(self, ctx, *, username):
        """Shows an osu! User Stats!"""

        apikey = await self.config.apikey()

        if apikey is None or apikey == "":
            await ctx.send("You need to set an API key to use the osu! API, please use [p]osukey")
            return

        # Queries api to get osu profile
        headers = {"content-type": "application/json", "user-key": apikey}

        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://osu.ppy.sh/api/get_user?k={apikey}&u={username}", headers=headers) as response:
                osu = await response.json()

        if osu:
            SSH = "<:RankSSH:926177230357405736>"
            SS = "<:RankSS:926177315757645844>"
            SH = "<:RankSH:926177357834895370>"
            S = "<:RankS:926177374196875284>"
            A = "<:RankA:926177386737848321>"

            # Format stolen from owo#0498's ">osu" command. (Thanks Stevy 😹)
            joined = "**▸ Joined at:** {}\n".format(osu[0]["join_date"][:10])
            rank = "**▸ Rank:** #{}".format(humanize_number(osu[0]["pp_rank"])) + " (:flag_{}: ".format(osu[0]["country"]).lower() + "#{})\n".format(humanize_number(osu[0]["pp_country_rank"]))
            level = "**▸ Level:** {}\n".format(osu[0]["level"][:5])
            pp = "**▸ PP:** {}\n".format(osu[0]["pp_raw"])
            acc = "**▸ Accuracy:** {} %\n".format(osu[0]["accuracy"][:6])
            playcount = "**▸ Playcount:** {}\n".format(humanize_number(osu[0]["playcount"]))
            playtime = "**▸ Playtime:** {}\n".format(humanize_timedelta(seconds=osu[0]["total_seconds_played"]))
            ranks = f"**▸ Ranks:** {SSH}" + "`{}`".format(osu[0]["count_rank_ssh"]) + f"{SS}" + "`{}`".format(osu[0]["count_rank_ss"]) + f"{SH}" + "`{}`".format(osu[0]["count_rank_sh"]) + f"{S}" + "`{}`".format(osu[0]["count_rank_s"]) + f"{A}" + "`{}`\n".format(osu[0]["count_rank_a"])
            rscore = "**▸ Ranked Score:** {}\n".format(humanize_number(osu[0]["ranked_score"]))
            tscore = "**▸ Total Score:** {} ".format(humanize_number(osu[0]["total_score"]))

            # Build Embed
            desc = f"{joined}{rank}{level}{pp}{acc}{playcount}{playtime}{ranks}{rscore}{tscore}"
            colour = await self.bot.get_embed_colour(await ctx.embed_color())

            embed = discord.Embed(description=f"{desc}", colour=colour)
            embed.set_author(
                icon_url="https://icon-library.com/images/osu-icon/osu-icon-16.jpg",
                url="https://osu.ppy.sh/u/{}".format(osu[0]["user_id"]),
                name="osu!Standard Profile for {}".format(osu[0]["username"])
            )
            embed.set_footer(text="Powered by osu!", icon_url="https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png")
            embed.set_thumbnail(url="https://a.ppy.sh/{}".format(osu[0]["user_id"]))
            await ctx.send(embed=embed)
        else:
            await ctx.send("No results.")

    @commands.command(aliases=["osuimg"])
    @commands.bot_has_permissions(embed_links=True)
    async def osuimage(ctx, username:str):
        """Shows an osu! User Stats with Image!""" # Thanks epic, thanks preda <3
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get(f"https://api.martinebot.com/v1/imagesgen/osuprofile?player_username={username}") as resp:
                    if resp.status in (200,201):
                        f = discord.File(fp=BytesIO(await resp.read()), filename=f"osu.png")
                        embed = discord.Embed(title=f"{username}'s Osu Stats", colour=await ctx.embed_colour())
                        embed.set_image(url="attachment://osu.png")
                        embed.set_footer(text="Powered by martinebot.com API")
                        await ctx.send(file=f,embed=embed)
                        f.close()
                    elif resp.status in (404,410,422):
                        await ctx.send((await resp.json())['message'])
                    else:
                        await ctx.send("API is currently down, please try again later.")

    @commands.command()
    @checks.is_owner()
    async def osukey(self, ctx, key):
        """Set osu! API key"""

        # Load config
        config_boards = await self.config.apikey()

        # Set new config
        await self.config.apikey.set(key)
        await ctx.send("The API key has been added.")