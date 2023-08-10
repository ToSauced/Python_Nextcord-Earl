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
    
    @commands.command(name="bug")
    async def bug(self, ctx):
        await ctx.reply(f"{self.calculateTime()}")
        return

    @commands.command(name="donate")
    async def donate(self, ctx):
        await ctx.reply("A")
        return
    
    @commands.command(name="welcome")
    async def welcome(self, ctx):
        # Make sure default welcome message is disabled or replace 
        return
    @commands.command(name="joindm")
    async def joindm(self, ctx, *, args):
        # disabled by default: DM message that is sent to the user on join
        # TODO: create the listener

        return 
    
    @commands.command(name="enable")
    async def enable(self, ctx, *, args):
        return
    @commands.command(name="disable")
    async def disable(self, ctx, *, args):
        return
    
    @commands.command(name="restrict")
    async def restrict(self, ctx, *, args):
        return
    @commands.command(name="unrestrict")
    async def unrestrict(self, ctx, *, args):
        return
    
    @commands.command(name="modonly")
    async def modonly(self, ctx, *, args):
        return
    @commands.command(name="unmodonly")
    async def unmodonly(self, ctx, *, args):
        return
    
    @commands.command(name="ignore")
    async def ignore(self, ctx, *, args):
        args = str(args).split(" ")
        return
    @commands.command(name="unignore")
    async def unignore(self, ctx, *, args):
        args = str(args).split(" ")
        return
    
    @commands.command(name="prefix")
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

    @commands.command(name="help")
    async def help(self, ctx):

        embed=nextcord.Embed(title="Commands",color=nextcord.Color.light_gray())

        for command in self.bot.commands:
            # hidden commands (e.g., from cogs)
            if command.hidden:
                continue
            
            name = command.name
            description = command.help or "No description avaliable."

            embed.add_field(name=name, value=description, inline=False)
        await ctx.reply(embed=embed)

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
            member = ctx.author

        # Define user information

        # Construct user ID card (embed)
        embed = nextcord.Embed()

        # Send embed
        await ctx.send(embed=embed)
    
    @commands.command(name="nick",
                      usage="!nick [set,remove] (name) <member>")
    # description:
    async def nick(self, ctx, function: str, name: str = None, member: nextcord.Member = None):
        
        functions = ['set','remove']

        if function in functions:
            if function == functions[0]:
                
                if member is None:
                    member = ctx.author
                if member.joined_at is not None:
                    if name is not None & name.isascii:
                        member.edit(nick=name)
                        response = f"{member.name}'s nickname has been set to **{name}**"
                    else:
                        response = f"{name} is made up of invalid characters."
                else:
                    response = f"{member.name} has never joined the server!"
        
        if function is None:
            # self nickname status check
            if member.nick == member.name:
                response = "No nickname is currently applied to you."
            else:
                response = f"Current nickname: **{member.nick}**"

        await ctx.send(response)

    @commands.command(name="invite")
    async def invite(self,ctx):
        # action: invite [bot or server]
        # description: generate an invite for bot or for the discord server
        await ctx.send("A")
    
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
    @commands.command(aliases=['membercount','usercount'])
    # description: get the server member count (includes bot by default), if true or humans it only returns true members
    # usage: !membercount ('humans' or 'true')
    async def guildsize(self,ctx):
        await ctx.send("A")
    
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
