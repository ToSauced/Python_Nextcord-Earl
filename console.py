import bot.earl as earl
import os, re, yaml, inspect, datetime, threading

# yaml files
with open ('bot/config/settings.yaml','r') as file:
    data_settings = yaml.safe_load(file) # settings['value']
    bot_developer_settings = data_settings['settings']

with open ('bot/config/commands.yaml') as file:
    data_commands = yaml.safe_load(file) # commands['command']
    console_commands = data_commands['commands']

#=====================================================
# Console Command Functions 

def help():
    banner = "\n{< - " + "-" * 15 + " [HELP] "+ "-" * 15 + " - >}\n"
    print(banner)
    for command in console_commands:
        if command['enabled']:
            print(f"{command['label']}: {command['description']}")
            print(f"Aliases: {command['aliases']}")
            if 'flags' in command:
                print("Flags: ")
                for flag in command['flags']:
                    flag_name, flag_description = list(flag.items())[0]
                    print(f"    {flag_name}: {flag_description}")
        print("")
    print("-" * len(banner))

def servers():
    name_max_len = 0
    max_len = 0
    for guild in earl.bot.guilds:
        # TODO: make a function 'craftTable': creates separators between values input and a separation line
        if len(guild.name) > name_max_len:
            name_max_len = len(guild.name)
        message = f"{guild.name} | {guild.id}"
        if len(message) > max_len:
            max_len = len(message)
    print("\nName"+ " " * (name_max_len - 3) +"| ID")
    print("-" * max_len)
    for guild in earl.bot.guilds:
        print(f"{guild.name} | {guild.id}")
    print()
    
def server_info(args):
    for guild in earl.bot.guilds:
        # TODO: ID doesn't seem to be working, name works 
        if args[0] == guild.name.lower() or args[0] == guild.id:
            print()
            print(f"Verification Level: {guild.verification_level}")
            print(f"Owner: {guild.owner.name} (ID: {guild.owner.id})")

def exit():
    earl.logger.info("[Bot-Exit] Bot closed successfully, offline.")
    os._exit(0)

def clear():
    os.system("cls" if os.name=="nt" else "clear")

def uptime():
    current_time = datetime.datetime.now()

    bot_uptime = current_time - earl.start_time

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

    print(base)

#=====================================================
# Python Bot Console (back-end console)

def console_load(): # asthetic function (my bot dashboard?)
    print("\nWelcome\n")
    print("Use 'help' to get started!")
    print("Documentation: https://tosauced.duckdns.org/discordbot/docs\n")
    print(f"Servers: {len(earl.bot.guilds)+1}")
    #print("\nTODO: ")
    # todo list (top 3)
    print("")
    return
def exec_console():
    console_load()
    while True: # Python App Console 
        
        string = str(input(f"Earl [Console]: ")).lower()

        pattern = r'"([^"]+)"|(\S+)'

        search_string = re.findall(pattern, string)
        parameters = []
        # Makes it so we can pass strings as one value like "Tosauced enterprises"
        for quoted, non_quoted in search_string:
            if quoted:
                parameters.append(quoted)
            elif non_quoted:
                parameters.append(non_quoted)

        command = parameters[0]
        if len(parameters) > 1:
            arguments = parameters[1:]

        for qc in console_commands:
            if command == str(qc['label']) or command in qc['aliases']:
                if not qc['enabled']:
                    earl.logger.error(f"[Console-Command] '{command}' cannot be run, disabled command")
                    break
                earl.logger.info(f"[Console-Command] '{string}' executed")
                function_name = qc['action']
                exFunction = globals()[function_name]
                needed_parameters = len(inspect.signature(exFunction).parameters)
                if needed_parameters > 0:
                    exFunction(arguments)
                else:
                    exFunction()
                break
        else:
            earl.logger.error(f"[Console-Command] '{command}' cannot be run, not found")
            
#=======================================================
# -== INIT ==-

def main():
    earl.init_logger()
    # BOT_TOKEN file
    with open('bot/secure/token.key', 'r') as file:
        BOT_TOKEN = file.read().strip()
    bot_thread = threading.Thread(target=lambda: earl.bot.run(BOT_TOKEN))
    bot_thread.start()
    console_thread = threading.Thread(target=exec_console)
    console_thread.start()
    
    bot_thread.join()
    console_thread.join()
    return
if __name__ == "__main__":
    main()