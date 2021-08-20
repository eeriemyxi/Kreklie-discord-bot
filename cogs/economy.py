from discord.ext import commands
import discord
from deta import Deta
from extras.easy_embed import easyembed as embed
import os
deta = Deta(os.getenv('DATABASE_KEY'))
userdb = deta.Base('user_data')
class Economy(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(usage = '[User]', aliases = ('bal', 'wallet'), description = 'Shows your virtual balance.')
    async def balance(self, ctx, user: discord.User = None):
        if user: user = user.id
        else: user = ctx.author.id
        

def setup(bot):
    bot.add_cog(Economy(bot))