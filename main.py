import logging
import pkgutil
logging.basicConfig(level=logging.INFO)
logging.getLogger("discord").setLevel(logging.WARNING)
global log ; log = logging.info
log('Script Started.')
import discord, os
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from deta import Deta
log('Modules imported')
deta = Deta(os.getenv('DATABASE_KEY'))
guilddb = deta.Base('guild_data')
intents = discord.Intents.default()
intents.members, intents.messages, intents.reactions = True, True, True


def return_command(bot, msg):
    if msg.channel == discord.DMChannel:
        guildid = str(msg.guild.id)
        check = guilddb.get(guildid)
        if check and 'prefix' in check:
            prefix = check['prefix']
        else:
            prefix = guilddb.put(key=guildid, data={'prefix': 'kk '})['prefix']
        return commands.when_mentioned_or(prefix)(bot, msg)
    else: return commands.when_mentioned_or('kk ')(bot, msg)


client = commands.Bot(command_prefix=return_command,
                      help_command=commands.MinimalHelpCommand(),
                      intents=intents,
                      owner_id=os.getenv('OWNER_ID'),
                      activity=discord.Activity(type=discord.ActivityType.watching, name='kk help'))
for extension in pkgutil.iter_modules(['cogs']):
    client.load_extension(f'cogs.{extension.name}')
    log(f'Loaded cog: {str(extension.name).capitalize()}')
log('Trying to login.')
client.run(os.getenv('BOT_TOKEN'))