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

from typing import List, Optional, Union

import aiosu
import discord
import kuroutils
from aiosu.exceptions import APIException
from aiosu.models import Gamemode, OAuthToken, User
from aiosu.utils import auth
from discord.utils import format_dt
from redbot.core.bot import Red
from redbot.core.commands import Context
from redbot.core.utils.chat_formatting import bold, humanize_number, humanize_timedelta, inline

from .constants import GAME_MODES, MODE_EMOJIS, RANK_EMOJIS
from .helpers import *

# Authentication Views


class AuthenticationModal(discord.ui.Modal):
    def __init__(self, *, timeout: int) -> None:
        super().__init__(title="Link Your osu! Account", timeout=timeout)
        self.authenticated = False
        self.user_token: Optional[OAuthToken] = None

        self.input = discord.ui.TextInput(
            label="Link",
            style=discord.TextStyle.paragraph,
            placeholder="Paste the link here",
            required=True,
        )
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction[Red]) -> None:
        osu_tokens = await interaction.client.get_shared_api_tokens("osu")
        tokens = (
            osu_tokens.get("client_id"),
            osu_tokens.get("client_secret"),
            osu_tokens.get("redirect_uri", "http://localhost/"),
        )
        url = self.input.value.strip()
        if tokens[-1] not in url:
            await interaction.response.send_message("Invalid URL provided.", ephemeral=True)
            return
        try:
            code = parse_code_from_url(url)
            self.user_token = await auth.process_code(*tokens, code)
        except Exception as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return
        self.authenticated = True
        await interaction.response.send_message(
            "Your osu! account has been linked.", ephemeral=True
        )
        self.stop()


class AuthenticationView(discord.ui.View):
    def __init__(self, auth_url: str, *, timeout: int) -> None:
        super().__init__(timeout=timeout)
        self.author: Optional[discord.User] = None
        self.message: Optional[discord.Message] = None

        self.authenticated = False
        self.user_token: Optional[OAuthToken] = None

        self.link_button = discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="Click here to Authenticate your osu! account",
            url=auth_url,
        )
        self.add_item(self.link_button)

    @discord.ui.button(label="Link Account", style=discord.ButtonStyle.blurple)
    async def auth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = AuthenticationModal(timeout=self.timeout)
        await interaction.response.send_modal(modal)
        timed_out = await modal.wait()
        self.authenticated = modal.authenticated
        if not (timed_out or self.authenticated):
            return
        self.user_token = modal.user_token
        await self.disable_items()
        self.stop()

    async def start(self, ctx: Context, **kwargs) -> None:
        self.author = ctx.author
        embed = discord.Embed(color=await ctx.embed_color(), title="Link Your osu! Account")
        embed.add_field(
            name="How to Authenticate?",
            value=(
                "1. Click the button with the authentication link\n"
                "2. Make sure you are logged in to your osu! account\n"
                "3. Click on `Authorise`\n"
                "4. Copy the URL of the page you are redirected to\n"
                "5. Click on the `Link Account` button\n"
                "6. Paste the URL in the blank box\n"
            ),
        )
        kwargs = {
            "ephemeral": True,
            "reference": ctx.message.to_reference(fail_if_not_exists=False),
            "mention_author": False,
            "view": self,
        }
        if await ctx.embed_requested():
            kwargs["embed"] = embed
        else:
            kwargs["content"] = f"## {embed.fields[0].name}\n{embed.fields[0].value}"
        self.message = await ctx.send(**kwargs)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "You are not authorized to interact with this.", ephemeral=True
            )
            return False
        return True

    async def disable_items(self) -> None:
        for child in self.children:
            child.disabled = True
            if child.style != discord.ButtonStyle.link:
                child.style = discord.ButtonStyle.gray
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.disable_items()


# Profile Views


class ProfileModeSelect(discord.ui.Select["ProfileView"]):
    def __init__(self, *, default: Gamemode) -> None:
        options = [
            discord.SelectOption(label="Standard", value="0"),
            discord.SelectOption(label="Taiko", value="1"),
            discord.SelectOption(label="Catch the Beat", value="2"),
            discord.SelectOption(label="Mania", value="3"),
        ]
        options[default.id].default = True
        for option in options:
            mode = Gamemode.from_type(int(option.value))
            option.emoji = discord.PartialEmoji(
                name=mode.name_full.split(" ")[0], id=MODE_EMOJIS[mode.name_short.lower()]
            )
        super().__init__(min_values=1, max_values=1, options=options, row=0)

    async def callback(self, interaction: discord.Interaction):
        for option in self.options:
            option.default = False
        value = int(self.values[0])
        self.options[value].default = True
        await interaction.response.edit_message(embed=self.view.embeds[value], view=self.view)


class ProfileView(discord.ui.View):
    def __init__(
        self,
        bot: Red,
        client: aiosu.v2.Client,
        player: Optional[Union[int, str]] = None,
        query_type: Literal["id", "username"] = "id",
        *,
        timeout: int,
    ):
        super().__init__(timeout=timeout)
        self.author: Optional[discord.User] = None
        self.client = client
        self.embeds: List[discord.Embed] = []  # [standard, taiko, ctb, mania]
        self.player = player
        self.query_type = query_type

        self.rank_emojis = RANK_EMOJIS
        for rank, emoji in self.rank_emojis.items():
            self.rank_emojis[rank] = maybe_get_emoji(bot, emoji, bold(rank.upper()))

    @discord.ui.button(style=discord.ButtonStyle.red, emoji="✖️", row=1)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await kuroutils.delete_message(interaction.message)

    async def get_player(self, *, mode: Optional[Gamemode] = None) -> User:
        kwargs = {}
        # Why are we doing this? Because this will throw a ValueError if a kwarg's value is None.
        if mode:
            kwargs["mode"] = mode
        if not self.player:
            return await self.client.get_me(**kwargs)
        kwargs["qtype"] = self.query_type
        return await self.client.get_user(self.player, **kwargs)

    # Might need defer before executing this since this will probably take a while :/
    async def make_modes_embeds(self) -> Optional[List[discord.Embed]]:
        embeds = []
        for mode in GAME_MODES:
            user = await self.get_player(mode=mode)
            stats = user.statistics
            color = int(user.profile_colour.lstrip("#"), 16) if user.profile_colour else None

            embed = discord.Embed(color=color or 14456996, timestamp=user.join_date)
            embed.set_author(
                name=f"{user.username}'s osu! {mode.name_full} Profile",
                url=f"{user.url}/{mode.name_api}",
                icon_url=f"https://assets.ppy.sh/old-flags/{user.country_code}.png",
            )
            embed.set_thumbnail(url=user.avatar_url)
            # First Row
            embed.add_field(
                name="Global Rank",
                value=f"#{maybe_humanize_number(stats.global_rank, 'Unknown')}",
            )
            if hr := user.rank_highest:
                embed.add_field(
                    name="Peak Rank",
                    value=f"#{humanize_number(hr.rank)}\n({format_dt(hr.updated_at, 'R')})",
                )
            else:
                embed.add_field(name="Peak Rank", value="#Unknown")
            embed.add_field(
                name="Country Rank",
                value=f"#{maybe_humanize_number(stats.country_rank, 'Unknown')}",
            )
            # Second Row
            embed.add_field(
                name="Level",
                value=str(stats.level.current + round(stats.level.progress / 100, 2)),
            )
            embed.add_field(name="PP", value=maybe_humanize_number(round(stats.pp, 2), "0"))
            embed.add_field(name="Accuracy", value=f"{round(stats.hit_accuracy, 2)}%")
            # Third Row
            embed.add_field(name="Play Count", value=maybe_humanize_number(stats.play_count, "0"))
            embed.add_field(name="Play Time", value=humanize_timedelta(seconds=stats.play_time))
            embed.add_field(
                name="Highest Combo", value=f"{maybe_humanize_number(stats.maximum_combo, '0')}x"
            )
            # Fourth Row
            embed.add_field(
                name="Grades",
                value=(
                    f"{self.rank_emojis['ssh']} {inline(maybe_humanize_number(stats.grade_counts.ssh, '0'))} "
                    f"{self.rank_emojis['ss']} {inline(maybe_humanize_number(stats.grade_counts.ss, '0'))} "
                    f"{self.rank_emojis['sh']} {inline(maybe_humanize_number(stats.grade_counts.sh, '0'))} "
                    f"{self.rank_emojis['s']} {inline(maybe_humanize_number(stats.grade_counts.s, '0'))} "
                    f"{self.rank_emojis['a']} {inline(maybe_humanize_number(stats.grade_counts.a, '0'))}"
                ),
                inline=False,
            )
            # Fifth Row
            embed.add_field(
                name="Total Hits", value=f"{maybe_humanize_number(stats.total_hits, '0')}x"
            )
            embed.add_field(
                name="Ranked Score", value=maybe_humanize_number(stats.ranked_score, "0")
            )
            embed.add_field(
                name="Total Score", value=maybe_humanize_number(stats.total_score, "0")
            )
            # Sixth Row
            embed.add_field(
                name="Followers", value=maybe_humanize_number(user.follower_count, "0")
            )
            embed.add_field(
                name="Medals", value=maybe_humanize_number(len(user.user_achievements), "0")
            )
            embed.add_field(
                name="Replays Watched",
                value=maybe_humanize_number(stats.replays_watched_by_others, "0"),
            )
            embed.set_image(url=user.cover.url)
            embed.set_footer(text="Joined osu! on")
            embeds.append(embed)

        return embeds

    async def start(self, ctx: Context) -> None:
        async with ctx.typing():
            try:
                player = await self.get_player()
            except APIException as e:
                if e.status == 404:
                    await ctx.send("User not found.", ephemeral=True)
                    return

            self.embeds = await self.make_modes_embeds()

        self.author = ctx.author
        self.add_item(ProfileModeSelect(default=player.playmode))
        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.link, label="View osu! Profile", url=player.url
            )
        )
        self.message = await ctx.send(
            embed=self.embeds[player.playmode.value],
            reference=ctx.message.to_reference(fail_if_not_exists=False),
            mention_author=False,
            view=self,
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "You are not authorized to interact with this menu.",
                ephemeral=True,
            )
            return False
        return True

    async def on_timeout(self) -> None:
        for child in self.children:
            if hasattr(child, "style") and child.style == discord.ButtonStyle.link:
                continue
            child.disabled = True
        await self.message.edit(view=self)
