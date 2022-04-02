from typing import Optional

import discord
from redbot.core import commands


def is_owner(real: Optional[bool], copied: Optional[bool]):
    async def predicate(ctx):
        if real:
            if ctx.author.id in ctx.bot.owner_ids:
                return True
        if copied:
            all_owner_ids = ctx.bot.get_cog("Sudo").all_owner_ids
            if ctx.author.id in all_owner_ids and ctx.author.id not in ctx.bot.owner_ids:
                return True
        return False
    return commands.check(predicate)