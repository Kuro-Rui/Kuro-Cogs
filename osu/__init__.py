from .osu import Osu


async def setup(bot):
    await bot.add_cog(Osu(bot))
