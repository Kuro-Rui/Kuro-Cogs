from .avatar_imgen import AvatarImgen


async def setup(bot):
    await bot.add_cog(AvatarImgen(bot))
