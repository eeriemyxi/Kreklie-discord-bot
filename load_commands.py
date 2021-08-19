from discord.ext import commands
from commands.fun import Fun
from commands.info import Information
from commands.utilities import Utilities
from events import Events
from commands.server import Server
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("discord").setLevel(logging.WARNING)
global log ; log = logging.info
class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

log('Loading cogs')
def setup(bot):
    bot.add_cog(Utilities(bot))
    log('Utilities cog added.')
    bot.add_cog(Fun(bot))
    log('Fun cog added.')
    bot.add_cog(Information(bot))
    log('Information cog added.')
    bot.add_cog(Events(bot))
    log('Events cog added.')
    bot.add_cog(Server(bot))
    log('Server cog added.')