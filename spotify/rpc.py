"""
MIT License

Copyright (c) 2017 TrustyJAID

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging

from redbot.core.bot import Red
from redbot.core.commands import commands

from dashboard.rpc.utils import rpccheck

log = logging.getLogger("red.trusty-cogs.spotify")


class DashboardRPC_Spotify:
    def __init__(self, cog: commands.Cog):
        self.bot: Red = cog.bot
        self.cog: commands.Cog = cog

        self.bot.register_rpc_handler(self.authenticate_user)

    def unload(self):
        self.bot.unregister_rpc_handler(self.authenticate_user)

    @rpccheck()
    async def authenticate_user(self, user: int, code: str, state: str):
        if not self.bot.get_cog("Spotify"):
            return {"status": 0, "message": "Spotify cog is not loaded."}

        user = int(user)  # Blame socket communication for this

        userobj = self.bot.get_user(user)
        if not userobj:
            return {"status": 0, "message": "Unknown user."}
        if not self.cog._credentials:
            return {"status": 0, "message": "Bot owner has not set credentials."}
        log.debug(user)
        try:
            auth = self.cog.temp_cache[userobj.id]
        except KeyError:
            return {
                "status": 0,
                "message": "You must authenticate using a link given by bot. If this fails try posting the full URL inside discord.",
            }

        user_token = await auth.request_token(code=code, state=state)
        await self.cog.save_token(userobj, user_token)

        del self.cog.temp_cache[userobj.id]
        self.cog.dashboard_authed.append(userobj.id)

        return {"status": 1}
