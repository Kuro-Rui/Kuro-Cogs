from .core import ReactTermino


async def setup(bot):
    global old_restart
    old_restart = bot.get_command("restart")
    if old_restart:
        bot.remove_command(old_restart.name)

    global old_shutdown
    old_shutdown = bot.get_command("shutdown")
    if old_shutdown:
        bot.remove_command(old_shutdown.name)

    await bot.add_cog(ReactTermino(bot))
