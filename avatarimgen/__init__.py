from .avatar_imgen import AvatarImgen


def setup(bot):
    bot.add_cog(AvatarImgen(bot))
