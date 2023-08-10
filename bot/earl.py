import nextcord, logging, asyncio, datetime, yaml, os
from nextcord.ext import commands

logger = logging.getLogger("bot_logger")
start_time = datetime.datetime.now()

# yaml files
with open ('bot/config/settings.yaml','r') as file:
    data_settings = yaml.safe_load(file) # settings['value']
    settings = data_settings['settings']

# Custom Cog from others to extend from
class BaseCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        return
    
    def calculateTimeStr(self) -> str:
        # formatted_time = time.strftime('%m/%d/%Y %H:%M:%S') military time
        formatted_time = self.calculateTime().strftime('%m/%d/%Y %I:%M:%S %p') # 12-hour time
        return formatted_time
    
    def calculateTime(self) -> datetime.datetime:
        desired_timezone_offset = datetime.timedelta(hours=-4)
        current_utc_time = datetime.datetime.utcnow()
        time = current_utc_time + desired_timezone_offset
        return time
    
    # To be called within commands, cleanup command message and response (reference Bot error_message_cleanup)
    def clean_command_message(self, message, reply) -> None:
        return

# Custom Bot for init functions, define baked-in listeners/commands
class BaseBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

        if self.get_command('help'):
            self.remove_command("help")
        self.add_bot_cogs()

        # remove all default commands / override
        # for command in self.commands:
        #     self.remove_command(command.name)

    # Load cogs 
    def add_bot_cogs(self):
        cog_dir = "./bot/cogs/"
        for filename in os.listdir(cog_dir):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f'bot.cogs.{filename[:-3]}') # import, remove .py extension
                except Exception as e:
                    print(f"Failed to load cog: {filename} => {e}")

    @staticmethod # clean up recieved/sent messages
    async def error_message_deletion(sleep_time: int, msg, reply):
        await asyncio.sleep(sleep_time)
        await msg.delete()
        await asyncio.sleep(sleep_time)
        await reply.delete()

    async def on_ready(self):
        logger.info(f'[Bot-Ready] Logged in as {bot.user.name} (ID: {bot.user.id})')

    async def on_guild_join(self, guild: nextcord.Guild):
        logger.info(f'[Bot-GuildJoin] {bot.user.name} has joined a new server {guild.name} (ID: {guild.id})')

    async def on_guild_remove(self, guild: nextcord.Guild):
        logger.info(f'[Bot-GuildLeave] {bot.user.name} has left {guild.name} (ID: {guild.id})')

    async def record_invoke(self, ctx):
        # TODO: (enabled/disable) delete command messages as they are sent
        # await ctx.message.delete() 'for example, shouldn't be done with 8ball, would'nt you wanna look back at your question?'
        logger.info(f"[Invoke-Command] {ctx.command} by {ctx.author} in {ctx.guild}.")
        logger.info(f"DEVELOPMENT {ctx.message} and, {ctx.reply}")
        return
    
    async def on_command_error(self, ctx, error):

        command = ctx.command
        string = ctx.message.content
        
        # Create bot instance to reference functions 
        bot_instance = BaseBot(command_prefix='!', intents=intents)

        try:
            if isinstance(error, commands.CommandNotFound):
                reply = await ctx.reply(f"Sorry, the command {command} doesn't seem to exist.")
                await bot_instance.error_message_deletion(5,ctx.message,reply)
            elif isinstance(error, commands.CommandOnCooldown):
                cooldown_remaining = error.retry_after
                minutes, seconds = divmod(cooldown_remaining, 60)
                reply = await ctx.reply(f"Slow down, !{command} is on a cooldown for {int(minutes)} minutes and {int(seconds)} seconds!")
                await bot_instance.error_message_deletion(3,ctx.message,reply)
            elif isinstance(error, commands.NoPrivateMessage):
                reply = await ctx.reply(f"'!{string}' must be executed inside of a server!")
                await bot_instance.error_message_deletion(60,ctx.message,reply)
            elif isinstance(error, commands.DisabledCommand):
                reply = await ctx.reply(f"!{command} is currently disabled by the developer or server moderators!")
                await bot_instance.error_message_deletion(5,ctx.message,reply)
            elif isinstance(error, commands.MaxConcurrencyReached):
                reply = await ctx.reply(f"!{command} is active by too many users, allow someone to finish. Bogus right?")
                await bot_instance.error_message_deletion(10,ctx.message,reply)
            elif isinstance(error, commands.CheckFailure):
                reply = await ctx.reply(f"Either your executing this in the wrong place, or shouldn't be doing so...")
                await bot_instance.error_message_deletion(3,ctx.message,reply)
            else:
                reply = await ctx.reply(f"An unhandled error occured: {error}")
                await bot_instance.error_message_deletion(10,ctx.message,reply)
        except nextcord.Forbidden: # 403 error
            print("[CommandError-Cleanup] Failed, attempting to remove message from Unauthorized channel (probably a DM)")
        except:
            await ctx.reply(f"An error occured: {error}")
            
def init_database(): # SQL connection definition
    return

def init_logger(): # Setting .log file and Console logging  (only referenced once)
    formatting = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_formatting = logging.Formatter('[%(levelname)s]: %(message)s')
    # Initalize
    logger = logging.getLogger("bot_logger")
    logger.setLevel(logging.INFO) # logging.levels: [debug, info, warning, error, critical]
    # Initalize Handlers
    logFile_handler = logging.FileHandler(f'bot.log') # log file output
    logFile_handler.setLevel(logging.INFO)
    logConsole_handler = logging.StreamHandler() # log console output
    logConsole_handler.setLevel(logging.ERROR)
    # Add Handlers to Logger
    logFile_handler.setFormatter(formatting)
    logConsole_handler.setFormatter(console_formatting)
    logger.addHandler(logFile_handler)
    logger.addHandler(logConsole_handler)

# Define Bot subscription to events, define the types of events your bot recieves
custom_prefixes = ['!','$'] # TODO: per server setting to set custom prefixes: uses server settings (prob SQL)
bot_prefix = commands.when_mentioned_or(*custom_prefixes)
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.message_content = True
intents.guilds = True
bot = BaseBot(command_prefix=bot_prefix, intents=intents)
async def before_invoke_callback(ctx):
    await bot.record_invoke(ctx)

for command in bot.commands:
    bot.before_invoke(before_invoke_callback)

# for command in bot.commands:
#     bot.before_invoke(command.before_invoke(bot.record_invoke))