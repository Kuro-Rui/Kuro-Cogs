from .fakemod import FakeMod


def setup(bot):
    bot.add_cog(FakeMod(bot))
