from .imgbb import ImgBB


async def setup(bot):
    await bot.add_cog(ImgBB(bot))
