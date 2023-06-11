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

import logging
from datetime import datetime, timezone
from typing import Literal, Mapping, Optional

import aiosu
import discord
from aiosu.exceptions import APIException
from aiosu.models import OAuthToken
from aiosu.utils import auth
from redbot.core import Config, commands
from redbot.core.app_commands import ContextMenu
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import humanize_list

from .abc import CompositeMetaClass
from .commands import OsuCommands
from .helpers import DEFAULT_RANK_EMOJIS

try:
    from .rpc import OsuDashboardRPC
except ImportError:
    DASHBOARD = False
else:
    DASHBOARD = True
from .views import AuthenticationView, ProfileView

log = logging.getLogger("red.kuro-cogs.osu")


class Osu(OsuCommands, commands.Cog, metaclass=CompositeMetaClass):
    """Commands for interacting with osu!"""

    __author__ = humanize_list(["Kuro"])
    __version__ = "0.0.3"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, identifier=32142)
        self.config.register_global(
            auth_timeout=300,
            menu_timeout=180,
            mode_emojis={"std": None, "taiko": None, "ctb": None, "mania": None},
            rank_emojis=DEFAULT_RANK_EMOJIS,
            scopes=["public", "identify"],
        )
        self.config.register_user(tokens={})

        self.authenticating_users = set()
        self._client_storage = None
        self._tokens = tuple()

        self.profile_ctx = ContextMenu(name="Get osu! Profile", callback=self.osu_profile_callback)
        self.bot.tree.add_command(self.profile_ctx)

        # RPC
        self.dashboard_authed = set()
        if DASHBOARD:
            self.rpc_extension = OsuDashboardRPC(self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Author  :` {self.__author__}\n"
            f"`Cog Version :` {self.__version__}"
        )

    async def cog_load(self) -> None:
        tokens = await self.bot.get_shared_api_tokens("osu")
        if not tokens:
            return
        self._tokens = (
            tokens.get("client_id"),
            tokens.get("client_secret"),
            tokens.get("redirect_uri", "http://localhost/"),
        )
        self._client_storage = aiosu.v2.ClientStorage(
            client_secret=self._tokens[1], client_id=self._tokens[0]
        )
        all_users = await self.config.all_users()
        if not all_users:
            return
        for i, config in all_users.items():
            if not config["tokens"]:
                continue
            token = OAuthToken.parse_obj(config["tokens"])
            await self._client_storage.add_client(token, id=i)

    async def cog_unload(self) -> None:
        if DASHBOARD:
            self.rpc_extension.unload()
        if self._client_storage:
            await self._client_storage.close()
        self.bot.tree.remove_command(self.profile_ctx.name, type=self.profile_ctx.type)

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ) -> None:
        await self.config.user_from_id(user_id).clear()

    async def _check(self, ctx: commands.Context, user: discord.User) -> bool:
        if not all(self._tokens):
            content = (
                "The bot owner needs to set osu! credentials before this command can be used.\n"
            )
            if await self.bot.is_owner(ctx.author):
                content += f"See `{ctx.clean_prefix}osu set creds` for more details."
            await ctx.send(content, ephemeral=True)
            return False
        if user.id in self.authenticating_users:
            await ctx.send(
                "Please complete your authorization first before using any commands.",
                ephemeral=True,
            )
            return False
        return True

    async def ask_for_auth(self, ctx: commands.Context, user: discord.User) -> None:
        check = await self._check(ctx, user)
        if not check:
            return
        auth_url = auth.generate_url(*self._tokens[::2])
        self.authenticating_users.add(user.id)
        embed = discord.Embed(
            color=await ctx.embed_color(),
            description="Click on the buttons below to authenticate your osu! profile.",
        )
        view = AuthenticationView(self, auth_url, timeout=await self.config.auth_timeout())
        if await ctx.embed_requested():
            await view.start(ctx, embed=embed)
        else:
            await view.start(ctx, embed.description)

    async def save_token(self, user: discord.User, token: OAuthToken) -> None:
        async with self.config.user(user).tokens() as tokens:
            tokens["access_token"] = token.access_token
            tokens["refresh_token"] = token.refresh_token
            tokens["expires_on"] = int(token.expires_on.timestamp())
            tokens["scopes"] = str(token.scopes).split(" ")

    async def get_client(
        self, ctx: commands.Context, user: discord.User = None
    ) -> Optional[aiosu.v2.Client]:
        user = user or ctx.author
        check = await self._check(ctx, user)
        if not check:
            return
        if not await self.config.user(user).tokens():
            return aiosu.v2.Client(client_id=self._tokens[0], client_secret=self._tokens[1])
        client = await self._client_storage.get_client(id=user.id)
        user_token = await client.get_current_token()
        expired = datetime.utcnow().timestamp() > user_token.expires_on.timestamp()
        if expired:
            try:
                # Token refreshing is actually handled by client by default,
                # but we need to handle so it's saved in the config and not just gone away.
                await client._refresh()
            except APIException:
                await ctx.send("Your token has been revoked, clearing data.", ephemeral=True)
                await self.config.user(user).tokens.clear()
                return
            await self.save_token(user, await client.get_current_token())
        return client

    async def osu_profile_callback(self, interaction: discord.Interaction, user: discord.Member):
        if not await self.config.user(user).tokens():
            await interaction.response.send_message(
                f"{user.mention} hasn't linked their osu! account yet.", ephemeral=True
            )
            return
        ctx = await commands.Context.from_interaction(interaction)
        client = await self.get_client(ctx, user)
        if not client:
            return
        config = await self.config.all()
        view = ProfileView(
            client,
            config["mode_emojis"],
            config["rank_emojis"],
            None,
            "string",
            timeout=config["menu_timeout"],
        )
        await view.start(ctx)

    @commands.Cog.listener()
    async def on_red_api_tokens_update(
        self, service_name: str, api_tokens: Mapping[str, str]
    ) -> None:
        if service_name == "osu":
            await self.cog_load()
