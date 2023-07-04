"""
MIT License

Copyright (c) 2021-present Kuro-Rui

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

# Taken from https://github.com/TrustyJAID/Trusty-cogs/blob/dpy-2.0/spotify/rpc.py

from typing import TYPE_CHECKING

from aiosu.utils import auth
from dashboard.rpc.utils import rpccheck
from redbot.core.bot import Red

if TYPE_CHECKING:
    from .osu import Osu


class OsuDashboardRPC:
    def __init__(self, cog: "Osu"):
        self.bot: Red = cog.bot
        self.cog: "Osu" = cog
        self.bot.register_rpc_handler(self.authenticate_user)

    def unload(self):
        self.bot.unregister_rpc_handler(self.authenticate_user)

    @rpccheck()
    async def authenticate_user(self, user: int, code: str):
        if not self.bot.get_cog("Osu"):
            return {"status": 0, "message": "Osu cog is not loaded."}
        if not (user_obj := self.bot.get_user(int(user))):
            return {"status": 0, "message": "Unknown user."}
        if not self.cog._tokens:
            return {"status": 0, "message": "Bot owner has not set credentials."}
        if user_obj.id not in self.cog.authenticating_users:
            return {
                "status": 0,
                "message": "You must authenticate using a link given by bot. If this fails try posting the full URL inside discord.",
            }

        user_token = await auth.process_code(*self.cog._tokens, code)
        await self.cog.save_token(user_obj, user_token)
        self.cog.authenticating_users.remove(user_obj.id)
        self.cog.dashboard_authed.add(user_obj.id)

        return {"status": 1}
