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

from io import BytesIO
from typing import Literal, Optional

import aiohttp
import discord
from aiosu.exceptions import APIException
from aiosu.models import Scopes
from redbot.core import app_commands, commands
from redbot.core.utils.chat_formatting import humanize_list, humanize_timedelta
from redbot.core.utils.views import SetApiView

from .abc import OsuMixin
from .views import ProfileView


class Commands(OsuMixin):
    """All the commands should be found here."""

    @commands.hybrid_group(name="osu")
    async def osu(self, ctx: commands.Context):
        """osu! related commands."""
        pass

    # Authentication commands

    @osu.command(name="link")
    async def osu_link(self, ctx: commands.Context):
        """Link your osu! account."""
        if not await self._config.user(ctx.author).tokens():
            await self.ask_for_auth(ctx)
            return
        await ctx.send(
            f"You already linked your osu! account. Use `{ctx.clean_prefix}osu unlink` to unlink your account.",
            ephemeral=True,
        )

    @osu.command(name="unlink")
    async def osu_unlink(self, ctx: commands.Context):
        """Unlink your osu! account."""
        if await self._config.user(ctx.author).tokens():
            await self._config.user(ctx.author).tokens.clear()
            await self._client_storage.revoke_client(ctx.author.id)
            await ctx.send("Your osu! account has been unlinked.", ephemeral=True)
            return
        await ctx.send(
            f"You haven't linked your osu! account. Use `{ctx.clean_prefix}osu link` to link your account.",
            ephemeral=True,
        )

    # User profile commands

    @commands.bot_has_permissions(embed_links=True)
    @osu.command(name="profile")
    @app_commands.describe(
        player="An osu! player username/id", query_type="The type of your query."
    )
    async def osu_profile(
        self,
        ctx: commands.Context,
        player: Optional[str] = None,
        query_type: Optional[Literal["id", "username"]] = "id",
    ):
        """Send a player's osu! profile in an embed."""
        client = await self.get_client(ctx)
        if not client:
            return

        if not (player or await client._token_exists()):
            await ctx.send(
                f"Please provide a username or link yourself with `{ctx.clean_prefix}osu link`",
                ephemeral=True,
            )
            return
        view = ProfileView(
            self.bot, client, player, query_type, timeout=await self._config.menu_timeout()
        )
        await view.start(ctx)

        if not await client._token_exists():
            await client.aclose()

    @commands.bot_has_permissions(attach_files=True)
    @commands.cooldown(60, 60, commands.BucketType.default)
    @osu.command(name="card")
    @app_commands.describe(player="An osu! player username")
    async def osu_card(self, ctx: commands.Context, player: Optional[str] = None):
        """Get a player's osu! Standard profile card."""
        if not player:
            client = await self.get_client(ctx)
            if not client:
                return
            if not await client._token_exists():
                await ctx.send(
                    f"Please provide a username or link yourself with `{ctx.clean_prefix}osu link`",
                    ephemeral=True,
                )
                return
            user_obj = await client.get_me()
            player = user_obj.username

        session = aiohttp.ClientSession()
        async with ctx.typing():
            async with session.get(
                "https://api.martinebot.com/v1/imagesgen/osuprofile",
                params={"player_username": player},
            ) as response:
                if response.status == 201:
                    result = await response.read()
                    await ctx.send(file=discord.File(BytesIO(result), "card.png"))
                else:
                    result = await response.json()
                    await ctx.send(result["message"], ephemeral=True)
        await session.close()

    @commands.bot_has_permissions(embed_links=True)
    @osu.command(name="avatar")
    @app_commands.describe(player="An osu! player username/id")
    async def osu_avatar(self, ctx: commands.Context, player: Optional[str] = None):
        """Get a player's current osu! avatar."""
        await ctx.defer()
        client = await self.get_client(ctx)
        if not client:
            return

        if player:
            try:
                user_obj = await client.get_user(player)
            except APIException as e:
                if e.status == 404:
                    await ctx.send("User not found.", ephemeral=True)
                    return
        else:
            if not await client._token_exists():
                await ctx.send(
                    f"Please provide a username or link yourself with `{ctx.clean_prefix}osu link`",
                    ephemeral=True,
                )
                return
            user_obj = await client.get_me()

        embed = discord.Embed(
            colour=user_obj.profile_colour or 14456996, title=f"{user_obj.username}'s osu! Avatar"
        )
        embed.set_image(url=user_obj.avatar_url)
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="View Avatar",
                url=user_obj.avatar_url,
            )
        )
        await ctx.send(embed=embed, view=view)

    # Settings commands

    @commands.is_owner()
    @commands.group()
    async def osuset(self, ctx: commands.Context):
        """osu! settings."""
        pass

    @osuset.command(name="creds")
    async def osuset_creds(self, ctx: commands.Context):
        """Instructions to set osu! API credentials."""
        description = (
            "1. Log in to your osu! account and go to https://osu.ppy.sh/home/account/edit\n"
            '2. Scroll down to "OAuth" and click on "New OAuth Appplication"\n'
            "3. Fill out the form provided with your app name and redirect uri (http://localhost/)\n"
            '4. Click on "Register application"\n'
            "5. Copy your client ID and your client secret into:\n"
            "`{prefix}set api osu client_id <your_client_id_here> client_secret <your_client_secret_here>`\n"
            "You may also provide `redirect_uri` (optional), the default redirect_uri is http://localhost/\n\n"
            "Note: The redirect URI Must be set in the form and must match either "
            "`http://localhost/` or the one you set with the `[p]set api` command."
        ).format(prefix=ctx.prefix)
        default_keys = {"client_id": "", "client_secret": "", "redirect_uri": "http://localhost/"}
        view = SetApiView("osu", default_keys)
        if await ctx.embed_requested():
            embed = discord.Embed(description=description)
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send(description, view=view)

    @osuset.command(name="authtimeout")
    async def osuset_auth_timeout(self, ctx: commands.Context, timeout: int):
        """
        Set the timeout for authentication.

        The default authentication timeout is 5 minutes (300 seconds)
        """
        await self._config.auth_timeout.set(timeout)
        await ctx.tick(
            message=f"Authentication timeout set to {humanize_timedelta(seconds=timeout)}."
        )

    @osuset.command(name="menutimeout")
    async def osuset_menu_timeout(self, ctx: commands.Context, timeout: int):
        """
        Set the timeout for the menu.

        The default menu timeout is 3 minutes (180 seconds)
        """
        await self._config.menu_timeout.set(timeout)
        await ctx.tick(message=f"Menu timeout set to {humanize_timedelta(seconds=timeout)}.")

    @osuset.command(name="scopes")
    async def osuset_scopes(self, ctx: commands.Context, *scopes: str):
        """
        Set customized scopes for what you want your bot to allow.
        This will send current scopes if no scopes are provided.

        Available options are:
        - public
        - identify
        - friends.read
        - forum.write
        - delegate
        - chat.write
        - lazer (currently not usable)

        You can find more information here: https://osu.ppy.sh/docs/index.html#scopes
        """
        if not scopes:
            scopes = await self._config.scopes()
            await ctx.send(f"Current scopes: {humanize_list(scopes)}")
            return
        try:
            scopes_obj = Scopes.from_api_list(scopes)
        except KeyError as e:
            await ctx.send(f"Invalid scope: {e}")
            return
        new_scopes = str(scopes_obj).split(" ")
        async with self._config.scopes() as current_scopes:
            current_scopes.clear()
            current_scopes.extend(new_scopes)
        await ctx.tick(message=f"Scopes has been set to: {humanize_list(new_scopes)}")
