import discord, os
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, CommandNotFound, MissingRequiredArgument, RoleNotFound
from deta import Deta
from extras.easy_embed import easyembed
import traceback

deta = Deta(os.getenv('DATABASE_KEY'))
userdb = deta.Base('user_data')
guilddb = deta.Base('guild_data')


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(embed=discord.Embed(
                color=easyembed.getcolor(ctx=ctx),
                title='Not found',
                description=
                f'Command not found. Try this instead: `{ctx.prefix}help`'))
        elif isinstance(error, RoleNotFound):
            await ctx.send(embed=discord.Embed(color=easyembed.getcolor(ctx),
                                               title='Not found',
                                               description=f'Role not found.'))
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(color = easyembed.getcolor(ctx),title = 'Missing required argument', description = f'Something is missing. Please have a look at the message below. You forgot to include `{error.param}`').add_field(name = 'How to use it: ', value = f"{ctx.prefix}{ctx.command} {ctx.command.signature}"))
        elif isinstance(error, CheckFailure):
            pass
        else:
            if hasattr(ctx.command, 'on_error'):
                return
            error_type = type(error)
            error_traceback = error.__traceback__
            error = "".join(traceback.format_exception(error_type, error, error_traceback))
            await ctx.send(f"""```py\n{error}```""")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        # await self.client.process_commands(ctx)

    @commands.Cog.listener()
    async def on_guild_join(guild):
        guildid = str(guild.id)
        check = guilddb.get(guildid)
        if check and 'prefix' in check:
            return
        else:
            guilddb.put(key=guildid, data={'prefix': 'kk '})
def setup(bot):
    bot.add_cog(Events(bot))