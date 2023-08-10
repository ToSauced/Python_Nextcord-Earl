# Python Discord Bot using nextcord

## https://docs.nextcord.dev/en/stable/

### Overview
I intend to make this as a base for more bots with simple implementation

Adding Cogs:
- Create a cog.py file and define the setup function, load your cogs there and the bot will load the file as long as it is in the /cogs directory

### For me mostly:
Dependencies are installed in a virtual environment
To use (run commands in project folder):
Windows: venv/Scripts/activate
Linux: source venv/bin/activate

Running the bot: python earl.py 
- This logs the bot into discord, connects to servers, and awaits commands/events

Bot Settings (in settings.json) are to be edited by console.py only 