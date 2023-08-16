# Python Discord Bot using nextcord

## https://docs.nextcord.dev/en/stable/

### Overview
I intend to make this as a base for more bots with simple implementation, even with a backend console running in a console on the machine (interactive).

If you were to download this code right now, just create a /secure/ directory inside of the /bot/ and put your bot token in a token.key file, should work successfully. 

Bot Settings (in settings.yaml) are to be edited by console.py only 

Uses mySQL as the database, all server(s) settings, options, and data are stored on a mySQL server.

Adding Cogs:
- Create a cog.py file and define the setup function, load your cogs there and the bot will load the file as long as it is in the /cogs directory

### For me mostly:
Dependencies are installed in a virtual environment
To use (run commands in project folder):
Windows: venv/Scripts/activate
Linux: source venv/bin/activate

Running the bot: python earl.py 
- This logs the bot into discord, connects to servers, and awaits commands/events