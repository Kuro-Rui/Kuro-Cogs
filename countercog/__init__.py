from .counter import CounterCog


async def setup(bot):
    await bot.add_cog(CounterCog(bot))
