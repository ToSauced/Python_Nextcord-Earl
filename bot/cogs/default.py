# default command&events (ALWAYS INCLUDED w/ bot)
import nextcord, asyncio, datetime
from nextcord.ext import commands
from bot import earl

start_time = datetime.datetime.now()
    
class Buttons(nextcord.ui.View):
    def __init__(self, *, timeout=5):
        super().__init__(timeout=timeout)
    @nextcord.ui.button(label="Button", style=nextcord.ButtonStyle.gray)
    async def gray_button(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
        await interaction.response.edit_message(content=f"This is an edited button response!")

class BotDefault(earl.BaseCog):
    def __init__(self,bot):
        super().__init__(bot) # reference BaseCog __init__ 
        return

    # example sending files:
    # @bot.command()
    # async def send_file(ctx):
    #     with open('example.txt', 'r') as file:
    #         await ctx.send(file=nextcord.File(file, filename='example.txt'))
    
    @commands.command(name="ads",
                      aliases=['advertisements'],
                      usage="!ads",
                      description="Timed Advertisements to display on the server, manage them here.",
                      enabled=False,
                      guild_only=True)
    async def ad(self, ctx):
        # TODO: timed messages (ads) saved per server in SQL as = id|message|cooldown
        return
    
    @commands.command(name="avatar",
                      aliases=["av"],
                      usage="!avatar [member]",
                      description="Replies with the avatar of the specified user",
                      enabled=True,
                      guild_only=False)
    # TODO: we could make it so we could pass multiple members, because why not, i.e., ctx.message.content.parse_mentions 
    async def avatar(self, ctx: commands.Context, *, args=None):
        
        if isinstance(ctx.channel, nextcord.TextChannel) or ctx.guild is not None:
            users = ctx.guild.parse_mentions(ctx.message.content) or []
        else:
            users = []
        
        try:
            if len(users) > 1:
                for user in users:
                    await ctx.author.send(f"{user.display_name}'s Avatar: {user.display_avatar}")
            else:
                if isinstance(ctx.channel, nextcord.DMChannel) or ctx.guild is None:
                    member = ctx.author
                elif len(users)==0: # no user specified, return self
                    member = ctx.author
                else:
                    member = users[0]
                    
                await ctx.author.send(f"{member.display_name}'s Avatar: {member.display_avatar}")
        except Exception as e:
            await ctx.reply(f"An error occurred while fetching the avatar: {e}")
        return
    
    @commands.command(name="bug",
                      aliases=[],
                      usage="!bug [message]",
                      description="Report an error with the bot, what happened (detailed, please)",
                      enabled=False,
                      guild_only=False)
    async def bug(self, ctx, *, message):
        # TODO: goes into SQL, one big table for all as = id|bug-message|user|timestamp
        await ctx.reply(f"Bug: '{message}'")
        return

    @commands.command(name="display",
                      aliases=[],
                      usage="!display ['members' or 'channels']",
                      description="Enable/Disable displaying server values w/ channels at the top.",
                      enabled=True,
                      guild_only=True)
    async def display(self, ctx, type=None):
        # TODO: server-settings SQL, as = setting(display-member-count)|t/f
        guild:nextcord.Guild = ctx.guild

        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),  # Lock the channel for everyone
        }

        # Values
        member_count = guild.member_count
        channel_count = len(guild.fetch_channels())

        # Add members value to a list of created ones
        # TODO: implement removing the channel
        if type == "members":
            channel = await guild.create_voice_channel(name=f"Members: {member_count}", overwrites=overwrites)
        elif type == "channels":
            channel = await guild.create_voice_channel(name=f"Channels: {channel_count}", overwrites=overwrites)
        else:
            await ctx.reply("Unknown type to display")
        return

    @commands.command(name="donate",
                      aliases=[],
                      usage="!donate",
                      description="Display a donate link for the developer",
                      enabled=False,
                      guild_only=False) # FINISHED 
    async def donate(self, ctx):
        await ctx.reply("I don't take any money, yet...")
        return
    
    @commands.command(name="welcome",
                      aliases=[],
                      usage="!welcome [enable/disable or 'message']",
                      description="Enabled/Disable, or set the welcome message for users entering the server!",
                      enabled=True,
                      guild_only=True)
    async def welcome(self, ctx):
        # Make sure default welcome message is disabled or replace 
        # TODO: implementation in SQL = setting(welcome_message)|message|t/f
        return
    @commands.command(name="joindm",
                      aliases=[],
                      usage="!joindm [enable/disable or 'message']",
                      description="Set a DM message to send users when they join the server",
                      enabled=True,
                      guild_only=True)
    async def joindm(self, ctx, *, args):
        # disabled by default: DM message that is sent to the user on join
        # TODO: implementation in SQL = setting(welcome_message)|message|t/f
        return 
    
    # PER SERVER BOT PREFIXES ?? How will I do this/restart the bot?
    @commands.command(name="prefix",
                      enabled=False)
    async def prefix(self, ctx, *, args):
        args = str(args).split(" ")
        if len(args) == 0:
            return # list enabled prefixes
        if (args[0]=="add"):
            return
        if (args[0]=="set"):
            return # remove all other prefixes, set it to defined one
        if (args[0]=="remove"):
            return
        if (args[0]=="clear"):
            return # reset to default 
        return

    @commands.command(name="help") # SENT THROUGH DM 
    async def help(self, ctx, icommand=None):

        bot: commands.Bot = self.bot
        if icommand is None:
            await ctx.message.delete()
            for cog in bot.cogs:
                embed=nextcord.Embed(title=f"{cog} Commands",color=nextcord.Color.light_gray())
                for command in bot.get_cog(cog).get_commands():
                    # hidden commands (e.g., from cogs)
                    command: commands.Command
                    if command.hidden:
                        continue
                    
                    name = command.name + f" {command.aliases}"
                    
                    description = command.description or "No description avaliable."
                    usage = command.usage or "No usage set."

                    description = f"""**Usage**: {usage}
                                    **Description**: {description}"""

                    embed.add_field(name=name, value=description, inline=False)
                await ctx.author.send(embed=embed)
        else:
            command = bot.get_command(icommand)
            help = command.help or f"No help message avaliable for {icommand}."
            await ctx.reply(help)

    @commands.command(name="ping")
    async def ping(self, ctx): # basically testing latency to me
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        await ctx.send(f"Pong! Latency: {latency} ms")
    
    @commands.command(name="github")
    async def github(self, ctx):
        await ctx.reply("https://github.com/ToSauced")
    
    @commands.command(name="self_info",
                      aliases=['binfo','info','about'])
    async def self_info(self, ctx):
        # embed is the fancy formatting
        embed = nextcord.Embed(title="Bot Information", description="This is an example embed.", color=nextcord.Colour.purple)
        embed.set_author()
        await ctx.send(embed=embed)
    
    @commands.command(name="uptime")
    # description: Get bot uptime
    async def self_uptime(self, ctx):

        current_time = datetime.datetime.now()
        bot_uptime = current_time - start_time
        
        days = bot_uptime.days
        hours, remainder = divmod(bot_uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        base = "Earl's current uptime is "
        if (days > 0):
            base += f"{days} days, "
        if (hours > 0):
            base += f"{hours} hours "
        if (minutes > 0):
            base += f"{minutes} minutes "

        base += f"{seconds} seconds "

        await ctx.send(base)
 

    @commands.command(name="whois",
                      usage="whois <member>")
    # description: Get user information
    async def whois(self,ctx, member: nextcord.Member = None):
        if member is None:
            member: nextcord.Member = ctx.author

        # Define user information
        name = member.display_name
        id = member.id
        roles = member.roles
        role_string = ""
        for role in roles:
            if roles[-1] != role:
                role_string += role.name+", "
            else:
                role_string += role.name
        avatar = member.display_avatar
        if member.activity is not None:
            status = member.activity.name
        else:
            status = "Nothing"
        if member.voice is not None:
            if member.voice.afk:
                is_afk = True
            else:
                is_afk = False
        else:
            is_afk = False

        # user 'tags'
        title = f"{name.upper()}"
        if is_afk:
            title += " [AFK_USER]"
        if member.bot:
            title += " [BOT]"


        # Construct user ID card (embed)
        embed = nextcord.Embed(title=title,
                               description=f"ID: {id}",
                               timestamp=self.calculateTime())

        embed.add_field(name="User Status",value=f"{status}",inline=False)
        embed.add_field(name="About",value=f"",inline=False)
        embed.add_field(name="Roles",value=f"{role_string}",inline=False)
        
        embed.set_image(avatar)

        # TODO: Add some buttons, like opening a chat w/ the user
        await ctx.send(embed=embed)
    
    @commands.command(name="nick",
                      usage="!nick [set,remove] (name) <member>")
    async def nick(self, ctx, *, args):
        # usage: !nick <function> [name] <user>, must use mentions in this context
        args = str(args).split(" ")

        users = ctx.guild.parse_mentions(ctx.message.content) or []

        functions = ['set','remove']

        await ctx.reply(f"{args}")

        if len(users) == 0:
            ctx.send(f"No user was specified")
            return
        member: nextcord.Member = users[0]
        if member is None or member.joined_at is None:
            member = ctx.author

        if args[0] in functions:
            if args[0] == functions[0]: # SET NICKNAME
                # TODO: if nickname is in quotes "" it puts the quotes as well, fix that
                if len(args) == 3:
                    await member.edit(nick=args[1])
                    response = f"Users name was successfully updated to **{args[1]}**"
                else:
                    response = f"Your really doin the most, redo it."

            if args[0] == functions[1]: # REMOVE NICKNAME
                await member.edit(nick=member.name)
                response = f"{member.name}'s nickname has been removed!"

        else:
            if member.nick == member.name:
                response = f"No nickname is currently applied to you."
            else:
                response = f"Current nickname: **{member.nick}**"

        await ctx.send(response)
        return

    @commands.command(name="invite")
    async def invite(self,ctx,type: str):
        # action: invite [bot or server]
        valid_types = ['server','bot']

        bot_invite = "https://discord.com/api/oauth2/authorize?client_id=1135022269295513721&permissions=8&scope=bot"
        if type == valid_types[0]:
            # Generate invite for current guild, or provide an existing link 
            return
        elif type == valid_types[1]:
            await ctx.reply(f"**Bot Invite**: {bot_invite}")

        return
    
    @commands.command(name="settings")
    async def settings(self, ctx):
        await ctx.send("A")
    
    @commands.command(name="update")
    async def update(self, ctx):
        # return Update information about the bot
        await ctx.send("A")
    
    @commands.command(name="support")
    async def support(self, ctx):
        # returns a discord link for a support server
        await ctx.send("A")
    
    @commands.command(name="reset")
    async def reset(self,ctx):
        await ctx.send("A")

    @commands.command(name="usage")
    # description: Will return the usages statistics for commands, for user
    async def usage(self,ctx):
        await ctx.send("A")

    @commands.command(name="website")
    async def website(self, ctx):
        embed = nextcord.Embed(title="tosauced.duckdns.org", url="https://tosauced.duckdns.org", color=nextcord.Colour.purple())
        #embed.set_image(url="https://tosauced.duckdns.org/resources/static/images/tosauced_logo.png")
        await ctx.reply(embed=embed)

    @commands.command(aliases=['serverinfo','iinfo','sinfo'])
    async def server_info(self, ctx):
        guild = ctx.guild
        if guild:
            # server info
            name = guild.name
            id = guild.id
            region = guild.region
            verification_level = guild.verification_level
            created_at = guild.created_at
            description = guild.description
            
            # returns arrays 
            channels = guild.channels
            users = guild.humans 

            await ctx.send(f"**Server Name**: {name} ({id})\n"
                           f"**Description**: {description}\n"
                           f"Region: {region}\n"
                           f"**Created At**: {created_at}\n"
                           f"Verification Level: {verification_level}\n"
                           # verify channels amount
                           f"Channels (#): {len(channels)-2}\n"
                           f"Users (#): {guild.member_count}\n"
                           f"Humans (#): {len(users)}"
                           )
        else:
            await ctx.reply("You must be in a server (to use this command)")
    
    @commands.command(name="gangs")
    async def gangs(self, ctx):
        return

# Development AREA

    @commands.command(name = "example",
                      aliases = ['ex'],
                      help="An example command.",
                      usage="!example",
                      description="An example command.",
                      enabled=True,
                      guild_only=False,
                      bot_has_permissions=['send_messages'])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member) # execution amount, cooldown time, who gets the cooldown?
    async def example(self, ctx):
        await ctx.send("This message has buttons!",view=Buttons())

def setup(bot): # referenced automatically when bot.load_extension
    bot.add_cog(BotDefault(bot))
    print("Cogs from Default.py loaded successfully.")
