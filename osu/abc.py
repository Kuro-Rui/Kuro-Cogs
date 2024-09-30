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
from typing import Optional, Set, Tuple

import aiosu
import discord
from redbot.core import Config, app_commands, commands
from redbot.core.bot import Red


class CompositeMetaClass(type(commands.Cog), type(ABC)):
    pass


class OsuMixin(ABC):
    def __init__(self, *_args) -> None:
        super().__init__(*_args)
        self.bot: Red
        self._client_storage: aiosu.v2.ClientStorage
        self._config: Config
        self._tokens: Tuple[str]

        self.authenticating_users: Set[int]
        self.profile_ctx: app_commands.ContextMenu

    @abstractmethod
    async def _init_tokens(self):
        raise NotImplementedError()

    @abstractmethod
    async def ask_for_auth(self, ctx: commands.Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_client(
        self,
        ctx: commands.Context,
        user: Optional[discord.User] = None,
        *,
        send_check: bool = True,
        use_token: bool = True,
    ) -> Optional[aiosu.v2.Client]:
        raise NotImplementedError()
