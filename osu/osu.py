import discord
from redbot.core import commands, Config, checks
import aiohttp
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS

BaseCog = getattr(commands, "Cog", object)


class Osu(BaseCog):
    """Show stuff using osu!"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=842364413)
        default_global = {"apikey": ""}
        self.config.register_global(**default_global)

    @commands.command()
    async def osu(self, ctx, *, username):
        """Shows an osu! user!"""

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

            joined = "**▸ Joined at:** " + osu[0]["join_date"][:10] + "\n"
            rank = "**▸ Rank:** #" + osu[0]["pp_rank"] + " (" + osu[0]["country"] + " #" + osu[0]["pp_country_rank"] + ")\n"
            level = "**▸ Level:** " + osu[0]["level"][:5] + "\n"
            score = "**▸ Total Score:** " + osu[0]["total_score"] + " (Ranked: " + osu[0]["ranked_score"] + ")\n"
            pp = "**▸ PP:** " + osu[0]["pp_raw"] + "\n"
            acc = "**▸ Accuracy:** " + osu[0]["accuracy"][:6] + "%\n"
            ranks = "**▸ Ranks:** " + f"{SSH}" + "`" + osu[0]["count_rank_ssh"] + "`" + f"{SS}" + "`" + osu[0]["count_rank_ss"] + "`" + f"{SH}" + "`" + osu[0]["count_rank_sh"] + "`" + f"{S}" + "`" + osu[0]["count_rank_s"] + "`" + f"{A}" + "`" + osu[0]["count_rank_a"] + "`" + "\n"
            playcount = "**▸ Playcount:** " + osu[0]["playcount"] + " (" + osu[0]["total_seconds_played"] + " s)"

            desc = f"{joined}{rank}{level}{score}{pp}{acc}{ranks}{playcount}"

            # Build Embed
            embed = discord.Embed()
            embed.description = f"{desc}"
            embed.set_author(
                icon_url="https://icon-library.com/images/osu-icon/osu-icon-16.jpg",
                url="https://osu.ppy.sh/u/{}".format(osu[0]["user_id"]),
                name="osu! Standard Profile for " + osu[0]["username"]
            )
            embed.set_footer(text="Powered by osu!", icon_url="https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png")
            embed.set_thumbnail(url="https://a.ppy.sh/{}".format(osu[0]["user_id"]))
            await ctx.send(embed=embed)
        else:
            await ctx.send("No results.")

    @commands.command()
    @checks.is_owner()
    async def osukey(self, ctx, key):
        """Set osu! API key"""

        # Load config
        config_boards = await self.config.apikey()

        # Set new config
        await self.config.apikey.set(key)
        await ctx.send("The API key has been added.")