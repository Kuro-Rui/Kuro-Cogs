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

from abc import ABC, abstractmethod
from typing import Literal, Mapping, Optional, Set, Tuple

import aiosu
import discord
from aiosu.models import OAuthToken
from kuroutils.converters import Emoji
from redbot.core import Config, app_commands, commands
from redbot.core.bot import Red

from .converters import Mode, Rank


class CompositeMetaClass(type(commands.Cog), type(ABC)):
    pass


class OsuMixin(ABC):
    def __init__(self, bot: Red) -> None:
        super().__init__(bot)
        self.bot: Red
        self._config: Config
        self.authenticating_users: Set[int]
        self._client_storage: aiosu.v2.ClientStorage
        self._tokens = Tuple[str]
        self.profile_ctx: app_commands.ContextMenu
        self.dashboard_authed = Set[int]

    @abstractmethod
    async def cog_load(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def cog_unload(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def _check(self, ctx: commands.Context, user: discord.User) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def ask_for_auth(self, ctx: commands.Context, user: discord.User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def save_token(self, user: discord.User, token: OAuthToken) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_client(
        self, ctx: commands.Context, user: discord.User = None
    ) -> Optional[aiosu.v2.Client]:
        raise NotImplementedError()

    @abstractmethod
    async def osu_profile_callback(self, interaction: discord.Interaction, user: discord.Member):
        raise NotImplementedError()

    @abstractmethod
    async def on_red_api_tokens_update(
        self, service_name: str, api_tokens: Mapping[str, str]
    ) -> None:
        raise NotImplementedError()

    # Commands

    @abstractmethod
    async def osu(self, ctx: commands.Context):
        raise NotImplementedError()

    @abstractmethod
    async def osu_link(self, ctx: commands.Context):
        raise NotImplementedError()

    @abstractmethod
    async def osu_unlink(self, ctx: commands.Context):
        raise NotImplementedError()

    @abstractmethod
    async def osu_profile(self, ctx: commands.Context, user: str = None, query_type: str = None):
        raise NotImplementedError()

    @abstractmethod
    async def query_type_autocomplete(self, interaction: discord.Interaction, current: str):
        raise NotImplementedError()

    @abstractmethod
    async def osu_card(self, ctx: commands.Context, user: str = None):
        raise NotImplementedError()

    @abstractmethod
    async def osu_avatar(self, ctx: commands.Context, user: str = None):
        raise NotImplementedError()

    @abstractmethod
    async def osu_set(self, ctx: commands.Context):
        raise NotImplementedError()

    @abstractmethod
    async def set_creds(self, ctx: commands.Context):
        raise NotImplementedError()

    @abstractmethod
    async def set_auth_timeout(self, ctx: commands.Context, timeout: int):
        raise NotImplementedError()

    @abstractmethod
    async def set_menu_timeout(self, ctx: commands.Context, timeout: int):
        raise NotImplementedError()

    @abstractmethod
    async def set_scopes(self, ctx: commands.Context, *scopes: str):
        raise NotImplementedError()

    @abstractmethod
    async def set_mode_emoji(self, ctx: commands.Context, mode: Mode, *, emoji: Emoji = None):
        raise NotImplementedError()

    @abstractmethod
    async def set_rank_emoji(self, ctx: commands.Context, rank: Rank, *, emoji: Emoji = None):
        raise NotImplementedError()
