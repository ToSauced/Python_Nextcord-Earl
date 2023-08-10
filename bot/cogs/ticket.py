from bot import earl
import nextcord
from nextcord.ext import commands

class Ticket(earl.BaseCog):
    # Description: Ticketing System of the bot
    # each ticket gets it own channel under the category 'Tickets'
    
    def __init__(self, bot):
        super().__init__(bot)
        return
    
    # Listeners 
    # - 
    #===
    
    # Commands
    # TODO: Determine if ticketing system should be under one command or multiple
    #===
    
    @commands.command(name="ticket")
    async def ticket(self, ctx, *, args=None):
        tickets_category_name = "Tickets" # TODO: can be changed by servers
        args = str(args).split(" ")
        
        tickets_category = next((category for category in ctx.guild.categories if category.name == f"{tickets_category_name}"), None)
        
        if tickets_category is None:
            await ctx.reply("Create a 'Ticket' category and submit your command there!")
            return
        
        if (ctx.channel.category.name != f"{tickets_category_name}"):
            await ctx.reply("Not in the tickets category")
            return
        
        # Create ticket category automatically with default name
        
        # Set the ticket category from an already created one 
        
        # Create a transcript of the current channel (last 1000 messages if that, create a temporary .txt submit to transcript channel)
        
        # Close Ticket from 'opened' stated
        
        # Re-Open Ticket from 'closed' state
        
        # Delete Ticket no matter the state
        
        # Rename the opened ticket channel (run in channel)
        
        return
        

def setup(bot):
    bot.add_cog(Ticket(bot))
    print("Cogs from Ticket.py loaded successfully.")
    return