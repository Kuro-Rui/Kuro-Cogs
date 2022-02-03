import asyncio
from asyncio import sleep
import datetime

import discord

from redbot.core import commands

class Polls(commands.Cog):
    """Just some Poll cog."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(add_reactions=True, embed_links=True, use_external_emojis=True)
    async def poll(self, ctx, question: str, option_1: str, option_2: str, option_3: str = None, option_4: str = None, option_5: str = None):
        """
        Create a poll with up to 5 options.
        You need atleast 1 message and 2 options.
        """
        # I mean... what do we need 10 options for?
        if len(question) > 256:
            await ctx.send("That question is too long.")
            return
        
        if option_3 is None:
            d = f":one: : {option_1}\n:two: : {option_2}"
        elif option_4 is None:
            d = f":one: : {option_1}\n:two: : {option_2}\n:three: : {option_3}"
        elif option_5 is None:
            d = f":one: : {option_1}\n:two: : {option_2}\n:three: : {option_3}\n:four: : {option_4}"
        else:
            d = f":one: : {option_1}\n:two: : {option_2}\n:three: : {option_3}\n:four: : {option_4}\n:five: : {option_5}"
        
        e = discord.Embed(title=question, description=d, color=await ctx.embed_color())
        e.set_footer(text=f"Poll by: {ctx.author}")
        e.timestamp = datetime.datetime.now(datetime.timezone.utc)

        message = await ctx.send(embed=e)
        one = "\N{DIGIT ONE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        two = "\N{DIGIT TWO}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        three = "\N{DIGIT THREE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        four = "\N{DIGIT FOUR}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        five = "\N{DIGIT FIVE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        if option_3 is None:
            await message.add_reaction(one)
            await message.add_reaction(two)
        elif option_4 is None:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
        elif option_5 is None:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
            await message.add_reaction(four)
        else:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
            await message.add_reaction(four)
            await message.add_reaction(five)

        msg = await ctx.send("✅ Poll created.")
        await sleep(3)
        try:
            await msg.delete()
        except discord.NotFound:
            return

        # ░░░░░░░░░░░░░░░░░░░░
        # ████████████████████