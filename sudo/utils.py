"""
Red - A fully customizable Discord bot
Copyright (C) 2017-present Cog Creators
Copyright (C) 2015-2017 Twentysix

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from redbot.core import commands


def is_owner(real: bool = False, copied: bool = False):
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
