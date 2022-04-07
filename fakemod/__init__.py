from .fakemod import FakeMod


async def setup(bot):
    await bot.add_cog(FakeMod(bot))
