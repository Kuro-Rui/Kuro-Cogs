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

import aiohttp
import discord
from aiosu.exceptions import APIException
from aiosu.models import Gamemode, Scopes
from redbot.core import app_commands, commands
from redbot.core.utils.chat_formatting import humanize_list, humanize_timedelta
from redbot.core.utils.views import SetApiView

from .abc import OsuMixin
from .converters import Emoji, Mode, QueryType, Rank
from .views import ProfileView


class OsuCommands(OsuMixin):
    @commands.hybrid_group(name="osu")
    async def osu(self, ctx: commands.Context):
        """Osu commands."""
        pass

    @osu.command(name="link")
    async def osu_link(self, ctx: commands.Context):
        """Link your osu! account."""
        if not await self.config.user(ctx.author).tokens():
            await self.ask_for_auth(ctx, ctx.author)
            return
        await ctx.send(
            f"You already linked your osu! account. Use `{ctx.clean_prefix}osu unlink` to unlink your account.",
            ephemeral=True,
        )

    @osu.command(name="unlink")
    async def osu_unlink(self, ctx: commands.Context):
        """Unlink your osu! account."""
        if await self.config.user(ctx.author).tokens():
            await self.config.user(ctx.author).tokens.clear()
            await self._client_storage.revoke_client(ctx.author.id)
            await ctx.send("Your osu! account has been unlinked.", ephemeral=True)
            return
        await ctx.send(
            f"You haven't linked your osu! account. Use `{ctx.clean_prefix}osu link` to link your account.",
            ephemeral=True,
        )

    @commands.bot_has_permissions(embed_links=True)
    @osu.command(name="profile")
    @app_commands.describe(user="An osu! user", query_type="The type of your query.")
    async def osu_profile(
        self, ctx: commands.Context, user: str = None, query_type: QueryType = None
    ):
        """Send a user's osu! profile in an embed."""
        client = await self.get_client(ctx)
        if not client:
            return
        if user and not query_type:
            try:
                user = int(user)
                query_type = "id"
            except ValueError:
                query_type = "string"
        if not user and not await client._token_exists():
            await ctx.send(
                f"Please provide a username or link yourself with `{ctx.clean_prefix}osu link`",
                ephemeral=True,
            )
            return
        config = await self.config.all()
        view = ProfileView(
            self.bot,
            client,
            config["mode_emojis"],
            config["rank_emojis"],
            user,
            query_type,
            timeout=config["menu_timeout"],
        )
        await view.start(ctx)

    @osu_profile.autocomplete("query_type")
    async def query_type_autocomplete(self, interaction: discord.Interaction, current: str):
        if not await interaction.client.allowed_by_whitelist_blacklist(interaction.user):
            return []

        choices = [
            app_commands.Choice(name="Username", value="string"),
            app_commands.Choice(name="User ID", value="id"),
        ]
        if current == "":
            return choices
        return [c for c in choices if current.lower() in c.name.lower()]

    @commands.bot_has_permissions(attach_files=True)
    @commands.cooldown(60, 60, commands.BucketType.default)
    @osu.command(name="card")
    async def osu_card(self, ctx: commands.Context, user: str = None):
        """Get a user's osu! Standard profile card."""
        await ctx.defer()
        if not user:
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
            user = user_obj.username
        session = aiohttp.ClientSession()
        async with session.get(
            f"https://api.martinebot.com/v1/imagesgen/osuprofile",
            params={"player_username": user},
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
    async def osu_avatar(self, ctx: commands.Context, user: str = None):
        """Get a user's current osu! avatar."""
        await ctx.defer()
        client = await self.get_client(ctx)
        if not client:
            return
        try:
            if not user:
                if not await client._token_exists():
                    await ctx.send(
                        f"Please provide a username or link yourself with `{ctx.clean_prefix}osu link`",
                        ephemeral=True,
                    )
                    return
                user_obj = await client.get_me()
            else:
                user_obj = await client.get_user(user)
        except APIException as e:
            if e.status == 404:
                await ctx.send("User not found.", ephemeral=True)
                return
        embed = discord.Embed(
            colour=user_obj.profile_colour or 14456996,
            title=f"{user_obj.username}'s osu! Avatar",
            timestamp=discord.utils.utcnow(),
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

    @commands.is_owner()
    @osu.group(name="set")
    async def osu_set(self, ctx: commands.Context):
        """Settings for Osu."""
        pass

    @osu_set.command(name="creds", with_app_command=False)
    async def set_creds(self, ctx: commands.Context):
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

    @osu_set.command(name="authtimeout", with_app_command=False)
    async def set_auth_timeout(self, ctx: commands.Context, timeout: int):
        """
        Set the timeout for authentication.

        The default authentication timeout is 5 minutes (300 seconds)
        """
        await self.config.auth_timeout.set(timeout)
        await ctx.tick(
            message=f"Authentication timeout set to {humanize_timedelta(seconds=timeout)}."
        )

    @osu_set.command(name="menutimeout", with_app_command=False)
    async def set_menu_timeout(self, ctx: commands.Context, timeout: int):
        """
        Set the timeout for the menu.

        The default menu timeout is 3 minutes (180 seconds)
        """
        await self.config.menu_timeout.set(timeout)
        await ctx.tick(message=f"Menu timeout set to {humanize_timedelta(seconds=timeout)}.")

    @osu_set.command(name="scopes", with_app_command=False)
    async def set_scopes(self, ctx: commands.Context, *scopes: str):
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
            scopes = await self.config.scopes()
            await ctx.send(f"Current scopes: {humanize_list(scopes)}")
            return
        try:
            scopes_obj = Scopes.from_api_list(scopes)
        except KeyError as e:
            await ctx.send(f"Invalid scope: {e}")
            return
        new_scopes = str(scopes_obj).split(" ")
        async with self.config.scopes() as current_scopes:
            current_scopes.clear()
            current_scopes.extend(new_scopes)
        await ctx.tick(message=f"Scopes has been set to: {humanize_list(new_scopes)}")

    @osu_set.command(name="modeemoji", with_app_command=False)
    async def set_mode_emoji(self, ctx: commands.Context, mode: Mode, *, emoji: Emoji = None):
        """Change an emoji used by the bot for showing modes."""
        async with self.config.mode_emojis() as mode_emojis:
            mode_emojis[mode.lower()] = emoji
        gm = Gamemode.from_type(mode)
        await ctx.tick()
        await ctx.send(f"Emoji for {gm.name_full} mode has been {'' if emoji else 're'}set.")

    @osu_set.command(name="rankemoji", with_app_command=False)
    async def set_rank_emoji(self, ctx: commands.Context, rank: Rank, *, emoji: Emoji = None):
        """Change an emoji used by the bot for showing ranks."""
        async with self.config.rank_emojis() as rank_emojis:
            rank_emojis[rank] = emoji
        await ctx.tick()
        await ctx.send(f"Emoji for {rank.upper()} rank has been {'' if emoji else 're'}set.")
