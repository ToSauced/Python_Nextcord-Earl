import nextcord, asyncio, datetime
from nextcord.ext import commands
from bot import earl


# [AUTOMOD]
class Automod(earl.BaseCog):
    def __init__(self, bot):
        self.bot = bot
        return
    
    # TODO: combined as of now (maybe make restricted nicknames/usernames seperate from blacklisted_words or check if word is in both lists)
    blacklisted_words = ['badword']
    restricted_usernames = []
    
    # Action to warn and record Moderation actions
    async def automod_log():
        # TODO: per server .log files? 
        # Get the log channel, submit message: if none defined, send DM to owner and abort

        return
    
    async def automod_check_message_content(self, message):
        
        # Check if message has attached file, check extension [!deletefiles]

        # Check Message content for blacklisted Words
        content = message.content.lower()

        if any(word in content for word in self.blacklisted_words):
            ctx = await self.bot.get_context(message)
            member = message.author
            await message.delete()
            await ctx.invoke(self.bot.get_command("warn"), member=member, reason="[Automod] Blacklisted word", bypass_warning=True)
        return
    
    async def automod_check_username(self, member: nextcord.Member):
        # check if username has blacklisted words, rename
        if any(word in member.display_name for word in self.blacklisted_words):
            # TODO: make this editable
            await member.edit(nick="Sanctioned User")
        return
    
    # Message listener
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return # ignore bot messages
        await self.automod_check_message_content(message=message)
    @commands.Cog.listener()
    async def on_message_edit(self, before, message):
        if message.author.bot:
            return # ignore bot mssages
        await self.automod_check_message_content(message=message)

    # Join Listener
    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        await self.automod_check_username(member)
        return
    # User Info Update
    @commands.Cog.listener()
    async def on_member_update(self, before: nextcord.Member, after: nextcord.Member):
        if before.display_name != after.display_name:
            await self.automod_check_username(after)
        return
    
    
    #===========================================
    # Automod Commands 

    @commands.command(name="automod",
                      enabled=True,
                      guild_only=True,
                      aliases=["am"],
                      description="Main command for Automod feature, encompases multiple features/commands.",
                      help="")
    @commands.has_permissions(administrator=True)
    async def automod(self, ctx, *, args = None):
        args: list = str(args).split(" ")
        # TODO: make a automod.yaml for this

        # Enable/Disable Automod 
        if (args[0]=="enable"):
            await ctx.reply("Automod is now **enabled**")
            return
        elif (args[0]=="disable"):
            await ctx.reply("Automod is now **disabled**")
            return
        
        # Set Automod Guard Channel
        if (args[0]=="guard"):
            return

        # Set Automod Log Channel
        if (args[0]=="log"):
            return

        # Set Automod Media Channel(s)
        if (args[0]=="media" or args[0]=="mo"):
            return
        if (args[0]=="unmedia" or args[0]=="umo" or args[0]=="unmo"):
            return

        # Automod Punishment w/ given Threshold
        if (args[0]=="punish" or args[0]=="punishment"):
            return

        # Ignore Whitelist (roles, channels, users)
        if (args[0]=="whitelist" or args[0]=="wl"):
            return
        return
    
    @commands.command(name="deletefiles",
                      enabled=True,
                      guild_only=True,
                      description="Toggle automatic deletion of unsafe files, only allowed file formats",
                      help="")
    async def deletefiles(self, ctx):
        return
    
    @commands.command()
    # description: will scan all the messages in the server, scanning them making sure they adhere to censoring rules
    async def scan(self, ctx):
        return

class ModerationCommands(earl.BaseCog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="mute")
    async def mute(self, ctx, member: nextcord.Member, time=None):
        return
    @commands.command(name="unmute")
    async def unmute(self, ctx, member: nextcord.Member):
        return
    @commands.command(name="muterole")
    async def muterole(self, ctx, *, args):
        return

    @commands.command(name="purge",
                      aliases=['delete','remove'])
    async def purge(self, ctx, amount: int):
        # purge (# of messages)
        if amount < 1:
            await ctx.send("Amount should be postive")
            return
        deleted_messages = await ctx.channel.purge(limit=amount + 1)
        dele_msg = await ctx.send(f"Deleted {len(deleted_messages) - 1} messages in {ctx.channel}.")
        await asyncio.sleep(3)
        await dele_msg.delete()
        
    @commands.command(name="warn")
    async def warn(self, ctx, member: nextcord.Member, *, reason=None, bypass_warning=False):

        if member == ctx.author and not bypass_warning:
            return
        if member == self.bot.user and not bypass_warning:
            await ctx.send("A")
            return
        if member == ctx.guild.owner and not bypass_warning:
            await ctx.send("A")
            return
        if reason is None:
            reason = "No reason was provided."
            
        embed=nextcord.Embed(title=f"{member.name} Warned",
                             color=nextcord.Color.yellow(),
                             timestamp=self.calculateTime())
        
        if bypass_warning:
            # TODO: repalce 'Bot' with a variable bot_name
            embed.set_footer(text=f"{earl.developer_settings['bot_name']}", icon_url='https://tosauced.duckdns.org/resources/static/images/tosauced_logo.png')
        else:
            embed.set_footer(text=f"{ctx.author}") # set the image to the avatar of the user who warned them
        embed.add_field(name="Reason", value=f"{reason}", inline=False)
        embed.add_field(name="Staff", value=f"{ctx.author}", inline=False)
        # TODO: make it so max_limit can be defined
        embed.add_field(name="Warnings Count", value=f"0/3", inline=False)
        
        await ctx.send(embed=embed)
        
    @commands.command(name="mail")
    async def mail(self, ctx, *, message=None):
        # description: send a DM to all users on the server (DM Alerts/Notifications)
        # TODO: make a subscribed check, if a user is unsubscribed don't send them the message
        
        if message == None:
            reply = await ctx.reply("Please provide a message")
            await self.bot.error_message_deletion(3, ctx.message, reply)
            return
        
        for member in ctx.guild.members:
            try:
                await member.send(message)
            except nextcord.Forbidden:
                await ctx.send(f"I couldn't send the message. {member.name} might have DMs disabled or blocked")
            except:
                await ctx.send(f"Couldn't send messsage to {member.name} for some reason?")
    
    @commands.command(name="kick")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        
        if member == ctx.author:
            await ctx.send("A")
            return
        if member == self.bot.user:
            await ctx.send("A")
            return
        if member == ctx.guild.owner:
            await ctx.send("A")
            return
        if reason is None:
            reason = "No reason was provided."
        
        await member.kick(reason=reason)
        
        embed = nextcord.Embed(title=f"{member.name} Kicked",color=nextcord.Colour.orange())
        
        embed.add_field(name="Reason", value=f"{reason}", inline=False)
        embed.add_field(name="Staff", value=f"{ctx.author}", inline=False)
        
        await ctx.send(embed=embed)
        
    @commands.command()
    async def lock(self, ctx):
        # lock [channel] (time) (message)
        await ctx.send("a")
        
    @commands.command()
    async def lockdown(self, ctx):
        # lockdown (message)
        # lockdown all channels, must be manually cancelled,started
        await ctx.send("a")

def setup(bot): # referenced automatically when bot.load_extension
    bot.add_cog(Automod(bot))
    bot.add_cog(ModerationCommands(bot))
    print("Cogs from Moderation.py loaded successfully.")