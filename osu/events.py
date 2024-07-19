from typing import Mapping

from redbot.core import commands

from .abc import OsuMixin


class Events(OsuMixin):
    """This contains listeners."""

    @commands.Cog.listener()
    async def on_red_api_tokens_update(
        self, service_name: str, api_tokens: Mapping[str, str]
    ) -> None:
        if service_name == "osu":
            await self._init_tokens()

    # Detect user and beatmap link on message later (coming soon...)
