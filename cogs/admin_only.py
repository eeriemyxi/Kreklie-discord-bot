import discord ; from discord.ext import commands
import os
from extras.easy_embed import easyembed
class AdminOnly(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    async def cog_check(self, ctx):
        if not str(ctx.author.id) == os.getenv('OWNER_ID'):
            await ctx.send(embed=easyembed.error("Missing permission", "Your user id doesn't match with the bot owner's specified user id.", ctx))
            return False
        return True
    @commands.command()
    async def reload(self, ctx, name: str):
        try:
            await ctx.send(embed = easyembed.error(
                f'Reloading cog "{name.capitalize()}"',
                "", ctx
            ))
            self.bot.reload_extension(f'cogs.{name}')
            await ctx.send(embed = easyembed.error(
                f'Cog "{name.capitalize()}" reloaded.',
                "", ctx
            ))
        except Exception: 
            await ctx.send(embed = easyembed.error(
                "Couldn't reload",
                "", ctx
            ))




def setup(bot):
    bot.add_cog(AdminOnly(bot))
