import asyncio
from asyncio import sleep
import datetime
from typing import Dict

import discord

from redbot.core import commands

class Polls(commands.Cog):
    """Just some Poll cog."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<question> <option_1> <option_2> [option_3] ... [option_10]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(add_reactions=True, embed_links=True, use_external_emojis=True)
    async def poll(
        self, 
        ctx, 
        question: str, 
        option_1: str, 
        option_2: str, 
        option_3: str = None, 
        option_4: str = None, 
        option_5: str = None,
        option_6: str = None,
        option_7: str = None,
        option_8: str = None,
        option_9: str = None,
        option_10: str = None
        ):
        """
        Create a poll with up to 10 options.
        You need atleast 1 message and 2 options.
        **Use `""` in every argument that is more than a word.**

        **Examples:** 
        • `[p]poll "Is this a poll?" Yes Maybe No`
        • `[p]poll "How are you?" Good "Not feeling well"`
        """
        # Totally not copying Dyno (jk I lied)

        if len(question) > 256:
            await ctx.send("That question is too long.")
            return
        
        one = "\N{DIGIT ONE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        two = "\N{DIGIT TWO}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        three = "\N{DIGIT THREE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        four = "\N{DIGIT FOUR}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        five = "\N{DIGIT FIVE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        six = "\N{DIGIT SIX}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        seven = "\N{DIGIT SEVEN}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        eight = "\N{DIGIT EIGHT}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        nine = "\N{DIGIT NINE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
        ten = "\N{KEYCAP TEN}"

        d1 = f"{one} : {option_1}\n\n{two} : {option_2}"
        d2 = f"{d1}\n\n{three} : {option_3}"
        d3 = f"{d2}\n\n{four} : {option_4}"
        d4 = f"{d3}\n\n{five} : {option_5}"
        d5 = f"{d4}\n\n{six} : {option_6}"
        d6 = f"{d5}\n\n{seven} : {option_7}"
        d7 = f"{d6}\n\n{eight} : {option_8}"
        d8 = f"{d7}\n\n{nine} : {option_9}"
        d9 = f"{d8}\n\n{ten} : {option_10}"
        
        if option_3 is None:
            d = d1
        elif option_4 is None:
            d = d2
        elif option_5 is None:
            d = d3
        elif option_6 is None:
            d = d4
        elif option_7 is None:
            d = d5
        elif option_8 is None:
            d = d6
        elif option_9 is None:
            d = d7
        elif option_10 is None:
            d = d8
        else:
            d = d9
        
        e = discord.Embed(title=question, description=d, color=await ctx.embed_color())
        e.set_footer(text=f"Poll by: {ctx.author}")
        e.timestamp = datetime.datetime.now(datetime.timezone.utc)

        message = await ctx.send(embed=e) # A really bad code right here
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
        elif option_6 is None:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
            await message.add_reaction(four)
            await message.add_reaction(five)
        elif option_7 is None:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
            await message.add_reaction(four)
            await message.add_reaction(five)
            await message.add_reaction(six)
        elif option_8 is None:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
            await message.add_reaction(four)
            await message.add_reaction(five)
            await message.add_reaction(six)
            await message.add_reaction(seven)
        elif option_9 is None:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
            await message.add_reaction(four)
            await message.add_reaction(five)
            await message.add_reaction(six)
            await message.add_reaction(seven)
            await message.add_reaction(eight)
        elif option_10 is None:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
            await message.add_reaction(four)
            await message.add_reaction(five)
            await message.add_reaction(six)
            await message.add_reaction(seven)
            await message.add_reaction(eight)
            await message.add_reaction(nine)
        else:
            await message.add_reaction(one)
            await message.add_reaction(two)
            await message.add_reaction(three)
            await message.add_reaction(four)
            await message.add_reaction(five)
            await message.add_reaction(six)
            await message.add_reaction(seven)
            await message.add_reaction(eight)
            await message.add_reaction(nine)
            await message.add_reaction(ten)

        msg = await ctx.send(embed=discord.Embed(description="✅ Poll created.", color=7844437))
        await sleep(5)
        try:
            await msg.delete()
        except discord.NotFound:
            return

        # ░░░░░░░░░░░░░░░░░░░░
        # ████████████████████