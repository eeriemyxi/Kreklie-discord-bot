from discord import guild
from discord.ext import commands
import discord, deta, os

deta = deta.Deta(os.getenv('DATABASE_KEY'))
guilddb = deta.Base('guild_data')


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        usage=f'<prefix> [withspace]',
        description=
        'Change the command prefix for this server. You need manage server permission to use this command. To reset it, enter `reset` as the prefix. To add a space after the prefix, you have to type "withspace" after entering the command.\nAll arguments combined and . as the prefix the command would look like this:\n<prefix>prefix . withspace'
    )
    async def prefix(self, ctx, prefix=None, withspace=None):
        if withspace:
            prefix += ' '
        if (ctx.author.guild_permissions.manage_guild
                or ctx.author.id == 858247195009482772) is False:
            return
        if not prefix:
            await ctx.send_help('prefix')
            return
        if prefix.lower() == 'reset':
            prefix = 'kk '
        if len(prefix) > 5:
            await ctx.send(embed=discord.Embed(
                title='The prefix is too long. It must be under 5 characters.')
                           )
            return
        guildid = str(ctx.guild.id)
        guilddb.update(key=guildid, updates={'prefix': prefix})
        await ctx.send(embed=discord.Embed(
            title='Done!',
            description=
            f'The prefix for this server has been updated to `{prefix}`.'))
        return