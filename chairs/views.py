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

import asyncio
from typing import List

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list, inline

# Believe it or not, all these views do the job :p


class StartingView(discord.ui.View):
    def __init__(self):
        self.cancelled = False
        self.players: List[discord.Member] = []
        super().__init__(timeout=None)

    @discord.ui.button(label="Join", style=discord.ButtonStyle.blurple)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.players:
            await interaction.response.send_message("You already joined the game.", ephemeral=True)
            return
        if len(self.players) >= 26:
            await interaction.response.send_message(
                "The maximum number of players has been reached.", ephemeral=True
            )
            return
        self.players.append(interaction.user)
        self.embed.description = f"Participants: {inline(str(len(self.players)))}"
        self.embed.set_field_at(
            0, name="Players", value=humanize_list([p.mention for p in self.players])
        )
        await self.message.edit(embed=self.embed)
        await interaction.response.send_message(
            "You have successfully joined the game!", ephemeral=True
        )

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.red)
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            await interaction.response.send_message("You are not in the game.", ephemeral=True)
            return
        self.players.remove(interaction.user)
        self.embed.description = f"Participants: {inline(str(len(self.players)))}"
        if self.players:
            self.embed.set_field_at(
                0, name="Players", value=humanize_list([p.mention for p in self.players])
            )
        else:
            self.embed.set_field_at(0, name="Players", value="None")
        await self.message.edit(embed=self.embed)
        await interaction.response.send_message(
            "You have successfully left the game!", ephemeral=True
        )

    async def start(self, ctx: commands.Context) -> discord.Message:
        self.ctx = ctx
        self.host = ctx.author
        self.embed = discord.Embed(
            color=await ctx.embed_color(),
            title="Chairs!",
            description=f"Participants: {inline('0')}",
            timestamp=discord.utils.utcnow(),
        )
        self.embed.add_field(name="Players", value="None")
        self.embed.set_footer(text="You have 60 seconds to join the game")
        kwargs = {
            "embed": self.embed,
            "reference": ctx.message.to_reference(fail_if_not_exists=False),
            "mention_author": False,
            "view": self,
        }
        self.message = await ctx.send(**kwargs)
        self.ctx.cog._cache[ctx.channel.id] = self
        await asyncio.sleep(60.0)
        await self.maybe_start_game()

    async def stop_game(self):
        self.cancelled = True
        self.stop()
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)
        self.ctx.cog._cache.pop(self.ctx.channel.id)

    async def maybe_start_game(self) -> discord.Message:
        if self.cancelled:
            return
        self.stop()
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)
        if len(self.players) < 2:
            self.ctx.cog._cache.pop(self.ctx.channel.id)
            await self.message.reply(
                "The game was cancelled because there aren't enough players to start the game."
            )
            return
        chairs = ChairsView(self.players)
        await chairs.start(self.ctx)


class ChairButton(discord.ui.Button):
    def __init__(self):
        super().__init__(disabled=True, emoji="\N{CHAIR}")
        self.taken = False

    async def callback(self, interaction: discord.Interaction):
        # We might need this to prevent the button thinks that
        # all people clicking at the same time is eligible to take the chair.
        if self.taken:
            await interaction.response.send_message("This chair is already taken.", ephemeral=True)
            return
        self.taken = True
        self.disabled = True
        self.view: ChairsView
        await self.view.message.edit(view=self.view)
        await interaction.response.send_message("You sat down!", ephemeral=True)
        self.view.winners.append(interaction.user)
        self.view.chairs -= 1
        if self.view.chairs == 0:
            await self.view.start_new_round()


class ChairsView(discord.ui.View):
    def __init__(
        self,
        players: List[discord.Member],
        losers: List[discord.Member] = [],
        current_round: int = 1,
    ):
        self.cancelled = False
        self.round = current_round
        self.players = players
        self.winners: List[discord.Member] = []
        self.losers = losers
        self.all_player_count = len(players)
        self.player_count = len(players) - len(losers)
        self.chairs = self.player_count - 1
        super().__init__(timeout=None)
        for _ in range(self.chairs):
            self.add_item(ChairButton())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in self.losers:
            await interaction.response.send_message("You already lose, mate.", ephemeral=True)
            return False
        if interaction.user not in self.players:
            await interaction.response.send_message("You are not in the game.", ephemeral=True)
            return False
        return True

    async def start(self, ctx: commands.Context) -> discord.Message:
        self.ctx = ctx
        self.host = ctx.author
        mentions = [p.mention for p in self.players]
        embed = discord.Embed(
            color=await ctx.embed_color(),
            title=f"Round {self.round} of Chairs!",
            description="Click on the chair before someone else does!",
        )
        embed.add_field(name="Players This Round", value=f"{self.player_count} players")
        embed.set_footer(text="Ready... Set...")
        kwargs = {"content": humanize_list(mentions), "embed": embed, "view": self}
        self.message = await ctx.send(**kwargs)
        self.ctx.cog._cache[ctx.channel.id] = self
        for child in self.children:
            child.disabled = False
        embed.set_footer(text="Go! Each player have 10 seconds to pick a chair.")
        await asyncio.sleep(2.0)  # Wait for 2 seconds before the game starts.
        await self.message.edit(embed=embed, view=self)
        await asyncio.sleep(10.0)
        # Prevent from starting a new round twice since
        # a new round will be started if all buttons are clicked
        if self.chairs > 0:
            await self.start_new_round()

    async def start_new_round(self):
        if self.cancelled:
            return
        self.stop()
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

        self.losers = [p for p in self.players if p not in self.winners]
        loser_mentions = [l.mention for l in self.losers]
        embed = discord.Embed(
            color=await self.ctx.embed_color(),
            title="Round Ended!",
            description=humanize_list(loser_mentions) + " lost this round!",
        )
        await self.message.reply(embed=embed)

        if len(self.winners) <= 1:
            await self.announce_winners()
            return

        chairs = ChairsView(self.players, self.losers, self.round + 1)
        async with self.ctx.typing():
            await asyncio.sleep(3)  # We don't want to rush, do we?
        await chairs.start(self.ctx)

    async def stop_game(self):
        self.cancelled = True
        self.stop()
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)
        self.ctx.cog._cache.pop(self.ctx.channel.id)

    async def announce_winners(self):
        mentions = [p.mention for p in self.players]
        if len(self.winners) == 1:
            embed = discord.Embed(
                color=await self.ctx.embed_color(),
                title=f"Winner!",
                description=f"The winner is {self.winners[0].mention} !",
            )
            embed.add_field(
                name="Rounds", value=f"{self.round} round" + ("s" if self.round > 1 else "")
            )
            embed.add_field(
                name=f"There are {self.all_player_count} players:",
                value=humanize_list(mentions),
                inline=False,
            )
            await self.message.reply(embed=embed)
            return
        # Somehow all people went afk (lmao?)
        elif len(self.winners) == 0:
            embed = discord.Embed(
                color=await self.ctx.embed_color(),
                title=f"No Winners!",
                description="There are no winners!",
            )
            embed.add_field(
                name="Rounds", value=f"{self.round} round" + ("s" if self.round > 1 else "")
            )
            embed.add_field(
                name=f"There are {self.all_player_count} players:", value=humanize_list(mentions)
            )
            await self.message.reply(embed=embed)
            return
        self.ctx.cog._cache.pop(self.ctx.channel.id)
