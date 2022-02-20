from .imgbb import ImgBB

def setup(bot):
    bot.add_cog(ImgBB(bot))