import discord ; from discord.ext import commands
import os, pkgutil
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
        if name.lower() == 'all':
            try:
                await ctx.send(embed = easyembed.error(
                    f'Reloading all cogs',
                    "", ctx
                ))
                logs = []
                log = logs.append
                for extension in pkgutil.iter_modules(['cogs']):
                    try: self.bot.reload_extension(f'cogs.{extension.name}')
                    except Exception as e: log(f'Failed to log cog {str(extension.name).capitalize()}. Error:\n{e}')
                    else: log(f'Reloaded cog: {str(extension.name).capitalize()}')
            except Exception: 
                await ctx.send(embed = easyembed.error(
                    "Couldn't reload",
                    "", ctx
                ))
            else:
                await ctx.send(embed = easyembed.simple(
                    'Reloaded all cogs. Logs:',
                    "\n".join(logs),
                    ctx
                ))
                return
        try:
            await ctx.send(embed = easyembed.error(
                f'Reloading cog "{name.capitalize()}"',
                "", ctx
            ))
        except Exception: 
            await ctx.send(embed = easyembed.error(
                "Couldn't reload",
                "", ctx
            ))
        else:
            self.bot.reload_extension(f'cogs.{name.lower()}')
            await ctx.send(embed = easyembed.error(
                f'Cog "{name.capitalize()}" reloaded.',
                "", ctx
            ))




def setup(bot):
    bot.add_cog(AdminOnly(bot))
