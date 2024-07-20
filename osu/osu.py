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

from typing import Literal, Optional

import aiosu
import discord
import kuroutils
from aiosu.exceptions import APIException
from aiosu.models import OAuthToken
from aiosu.utils import auth
from redbot.core import Config, commands
from redbot.core.app_commands import ContextMenu
from redbot.core.bot import Red

from .abc import CompositeMetaClass
from .commands import Commands
from .events import Events
from .views import AuthenticationView, ProfileView


class Osu(kuroutils.Cog, Commands, Events, metaclass=CompositeMetaClass):
    """Commands for interacting with osu!"""

    __author__ = ["Kuro"]
    __version__ = "0.1.2"

    def __init__(self, bot: Red) -> None:
        super().__init__(bot)
        self._config = Config.get_conf(self, 32142, True)
        self._config.register_global(
            auth_timeout=300, menu_timeout=180, scopes=["public", "identify"]
        )
        self._config.register_user(tokens={}, user_id=None)

        self.authenticating_users = set()
        self._client_storage = None
        self._tokens = tuple()

        self.profile_ctx = ContextMenu(name="Get osu! Profile", callback=self.osu_profile_callback)

    async def osu_profile_callback(self, interaction: discord.Interaction, user: discord.Member):
        ctx = await commands.Context.from_interaction(interaction)
        if not await self._config.user(user).tokens():
            await ctx.send(f"{user} hasn't linked their osu! account yet.", ephemeral=True)
            return False
        client = await self.get_client(ctx, user)
        if not client:
            return
        config = await self._config.all()
        view = ProfileView(self.bot, client, timeout=config["menu_timeout"])
        await view.start(ctx)

    async def _init_tokens(self):
        tokens = await self.bot.get_shared_api_tokens("osu")
        self._tokens = (
            tokens.get("client_id"),
            tokens.get("client_secret"),
            tokens.get("redirect_uri", "http://localhost/"),
        )
        if not all(self._tokens):
            return
        self._client_storage = aiosu.v2.ClientStorage(
            client_id=self._tokens[0], client_secret=self._tokens[1]
        )
        all_users = await self._config.all_users()
        if not all_users:
            return
        for user_id, config in all_users.items():
            if not config["tokens"]:
                continue
            token = OAuthToken.model_validate(config["tokens"])
            await self._client_storage.add_client(token, id=user_id)

    async def cog_load(self) -> None:
        await super().cog_load()
        await self._init_tokens()
        self.bot.tree.add_command(self.profile_ctx)

    async def cog_unload(self) -> None:
        super().cog_unload()
        if self._client_storage:
            await self._client_storage.aclose()
        self.bot.tree.remove_command(self.profile_ctx.name, type=self.profile_ctx.type)

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ) -> None:
        await self._config.user_from_id(user_id).clear()

    async def _check(self, author: discord.User) -> bool:
        if not all(self._tokens) or author.id in self.authenticating_users:
            return False
        return True

    async def _send_check(self, ctx: commands.Context) -> None:
        if not all(self._tokens):
            content = (
                "The bot owner needs to set osu! credentials before this command can be used."
            )
            if await self.bot.is_owner(ctx.author):
                content += f" See `{ctx.clean_prefix}osuset creds` for more details."
            await ctx.send(content, ephemeral=True)
            return
        if ctx.author.id in self.authenticating_users:
            await ctx.send(
                "Please complete your authorization first before using any commands.",
                ephemeral=True,
            )

    async def ask_for_auth(self, ctx: commands.Context) -> None:
        check = await self._check(ctx.author)
        if not check:
            await self._send_check(ctx)
            return

        auth_url = auth.generate_url(*self._tokens[::2])
        self.authenticating_users.add(ctx.author.id)
        view = AuthenticationView(auth_url, timeout=await self._config.auth_timeout())
        await view.start(ctx)
        timed_out = await view.wait()
        if not (timed_out or view.authenticated):
            return
        await self._save_token(ctx.author, view.user_token)
        self.authenticating_users.remove(ctx.author.id)
        await self._client_storage.add_client(view.user_token, id=ctx.author.id)

    async def _save_token(self, user: discord.User, token: OAuthToken) -> None:
        async with self._config.user(user).tokens() as tokens:
            tokens["access_token"] = token.access_token
            tokens["refresh_token"] = token.refresh_token
            tokens["expires_on"] = int(token.expires_on.timestamp())
            tokens["scopes"] = str(token.scopes).split(" ")

    async def _refresh_and_save_token(self, user: discord.User) -> None:
        client = await self._client_storage.get_client(id=user.id)
        await client._refresh()
        await self._save_token(user, await client.get_current_token())

    async def get_client(
        self,
        ctx: commands.Context,
        user: Optional[discord.User] = None,
        *,
        send_check: bool = True,
        use_token: bool = True,
    ) -> Optional[aiosu.v2.Client]:
        check = await self._check(ctx.author)
        if not check:
            if send_check:
                await self._send_check(ctx)
            return

        user = user or ctx.author
        if not (use_token and await self._config.user(user).tokens()):
            return aiosu.v2.Client(client_id=self._tokens[0], client_secret=self._tokens[1])

        client = await self._client_storage.get_client(id=user.id)
        user_token = await client.get_current_token()
        expired = discord.utils.utcnow().timestamp() > user_token.expires_on.timestamp()
        if expired:
            try:
                # Token refreshing is actually handled by the client by default,
                # but we need to make sure it's saved in the config and don't just go away.
                await self._refresh_and_save_token(user)
            except APIException:
                await ctx.send(
                    f"Your token has been revoked. Please do `{ctx.clean_prefix}osu link` again.",
                    ephemeral=True,
                )
                await self._config.user(user).tokens.clear()
                return
        return client
