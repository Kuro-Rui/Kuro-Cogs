from .osu import Osu


def setup(bot):
    bot.add_cog(Osu(bot))
