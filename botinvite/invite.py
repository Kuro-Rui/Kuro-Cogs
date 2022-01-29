import discord
from redbot.core import Config, checks, commands

old_invite = None


class BotInvite(commands.Cog):
    """
    Invite cog with an embed, multiple options, and buttons
    without using any extra libraries.
    """

    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return

    def __init__(self, bot):
        self.bot = bot
        default = {
            "support": False,
            "support_server": None,
            "description": "Thanks for choosing to invite {name} to your server!",
            "permissions": "",
            "applications_commands" : False
        }
        self.config = Config.get_conf(self, 376564057517457408, force_registration=True)
        self.config.register_global(**default)

    def cog_unload(self):
        global old_invite
        if old_invite:
            try:
                self.bot.remove_command("invite")
            except:
                pass
            self.bot.add_command(old_invite)

    @checks.is_owner()
    @commands.group(aliases=["inviteset", "invset"])
    async def invitesettings(self, ctx):
        """Settings for BotInvite cog."""
        pass

    @invitesettings.command()
    async def description(self, ctx, *, text: str = ""):
        """
        Set the embed description.
        Leave blank for default description
        Default: "Thanks for choosing to invite {name} to your server"
        Use `{name}` in your message to display bot name.
        Enter ``None`` to disable the description
        """
        if text == "":
            await self.config.description.clear()
            return await ctx.send("Embed Description set to default.")
        elif text == "None":
            await self.config.description.set("")
            return await ctx.send("Embed Description disabled.")
        await self.config.description.set(text)
        await ctx.send(f"Embed Description set to :\n`{text}`")

    @invitesettings.command()
    async def support(self, ctx, value: bool = None):
        """
        Choose if you want support field.
        Default: False
        """
        if value:
            await self.config.support.set(True)
            await ctx.send("Support Field set to `True`.")
        else:
            await self.config.support.set(False)
            await ctx.send("Support Field set to `False`.")

    @invitesettings.command()
    async def server(self, ctx, support_server):
        """
        Set a support server.
        Enter the invite link to your server.
        """
        await self.config.support_server.set(support_server)
        await ctx.send("Support Server set.")

    @invitesettings.command()
    async def setpermissions(self, ctx, *, value: int = ""):
        """Set the default permissions value for your bot.
        Get the permissions value from https://discordapi.com/permissions.html
        If left blank, resets permissions value to none
        Enter ``None`` to disable the permissions value
        """
        if value == "":
            await self.config.setpermissions.clear()
            return await ctx.send("Permissions Value reset.")
        elif value == "None":
            await self.config.setpermission.set("")
            return await ctx.send("Permissions Value disabled.")
        await self.config.setpermissions.set(value)
        await ctx.send("Permissions set.")

    @invitesettings.command()
    async def commandscope(self, ctx, value: bool = None):
        """
        ***Add the `applications.commands` scope to your invite URL.***
        
        This allows the usage of slash commands on the servers that invited your bot with that scope.

        Note that previous servers that invited the bot without the scope cannot have slash commands, they will have to invite the bot a second time.
        """
        if value:
            await self.config.applications_commands.set(True)
            await ctx.send("The `applications.commands` scope set to `True` and added to invite URL.")
        else:
            await self.config.applications_commands.set(False)
            await ctx.send("The `applications.commands` scope set to `False` and removed from invite URL.")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def invite(self, ctx):
        """
        Send personalized invite for the bot.
        """
        permissions = await self.config.setpermissions()
        server = await self.config.support_server()
        support = await self.config.support()
        applications_commands = await self.config.applications_commands()
        if server is None and support is True:
            return await ctx.send("Bot Owner needs to set a Support Server!")
        embed = discord.Embed(
            title="Thanks for inviting {name}!".replace("{name}", self.bot.user.name),
            description=(await self.config.description()).replace("{name}", self.bot.user.name),
            color=await ctx.embed_color(),
        )
        embed.set_author(
            name=ctx.bot.user.name, icon_url=ctx.bot.user.avatar_url_as(static_format="png")
        )
        embed.set_thumbnail(url=ctx.bot.user.avatar_url_as(static_format="png"))
        if applications_commands:
            embed.add_field(
                name="Bot Invite:",
                value="https://discord.com/oauth2/authorize?client_id={}&scope=bot+applications.commands&permissions={}".format(
                    self.bot.user.id, permissions
                ),
            )
        else:
            embed.add_field(
                name="Bot Invite:",
                value="https://discord.com/oauth2/authorize?client_id={}&scope=bot&permissions={}".format(
                    self.bot.user.id, permissions
                ),
            )
        if support:
            embed.add_field(name="Support Server:", value=f"[Click Here!]({server})", inline=True)
        embed.set_footer(text="{}".format(ctx.bot.user.display_name))
        
        await ctx.send(embed=embed)


def setup(bot):
    invite = BotInvite(bot)
    global old_invite
    old_invite = bot.get_command("invite")
    if old_invite:
        bot.remove_command(old_invite.name)
    bot.add_cog(invite)
