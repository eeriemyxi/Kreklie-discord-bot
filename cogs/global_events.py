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
    async def on_message_delete(self, ctx):
        if ctx.author.bot: return
        if check := userdb.get(str(ctx.author.id)):
            if 'ghostping' in check['settings'] and check['settings'][
                    'ghostping'] == 'off':
                return
        mentions = []
        for mention in ctx.raw_mentions:
            if mention == ctx.author.id: continue
            if check := userdb.get(str(mention)):
                if 'ghostping' in check['settings'] and check['settings'][
                        'ghostping'] == 'off':
                    continue
                else:
                    mentions.append(mention)
            else:
                user = self.client.get_user(mention)
                if user.bot: continue
                else: mentions.append(mention)
        if len(mentions) <= 0: return
        mentions = ', '.join([f'<@{i}>' for i in list(set(mentions))])
        embed = discord.Embed(
            color=easyembed.getcolor(ctx=ctx),
            title=f'{str(ctx.author)}',
            description=f'Ghost pinged {mentions}').set_footer(
                text=f'You can turn this off. Type: kk help settings')
        await ctx.channel.send(embed=embed)

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
            await ctx.send(embed=easyembed.error(
                'Missing required argument.',
                'Please have a look at the message below.', ctx))
            await ctx.send_help(ctx.command)
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