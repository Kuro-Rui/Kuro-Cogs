from .polls import Polls


async def setup(bot):
    await bot.add_cog(Polls(bot))


__red_end_user_data_statement__ = "This cog does not store any end user data."
