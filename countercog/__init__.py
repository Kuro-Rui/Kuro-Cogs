from .counter import CounterCog

def setup(bot):
    bot.add_cog(CounterCog(bot))