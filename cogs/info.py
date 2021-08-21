import json
from extras.easy_embed import easyembed
from discord.ext import commands
import discord
import typing


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def test(self, ctx, arg,arg1):
        pass
    @commands.command()
    async def userinfo(self,
                       ctx,
                       user: typing.Union[discord.Member,
                                          discord.User] = None):
        if not user: user = ctx.author

        if isinstance(user, discord.User): isUser = True
        else: isUser = None
        embed = discord.Embed(color=easyembed.getcolor(ctx),
                              title=f'User info about {user}')
        embed.add_field(name='Username', value=str(user), inline=False)
        embed.add_field(name='User ID', value=user.id)
        embed.add_field(name='Avatar URL', value=user.avatar_url, inline=False)
        if isUser is None:
            embed.add_field(name='Permissions',
                            value=', '.join([
                                name for name, value in user.guild_permissions
                                if value
                            ]),
                            inline=False)
            embed.add_field(name='Joined server at',
                            value=user.joined_at,
                            inline=False)
        else:
            pass
        embed.add_field(name='Joined discord at',
                        value=user.created_at,
                        inline=False)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(usage='@user',
                      description='View profile picture of users.')
    async def avatar(self,
                     ctx,
                     user: typing.Union[discord.User, discord.Member] = None):
        if not user: user = ctx.author
        embed = discord.Embed(color=easyembed.getcolor(ctx),
                              title=f'Avatar of {user}')
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def rolemembers(self, ctx, role: discord.Role):
        if len(role.members) > 0:
            text = ', '.join(['`' + str(i) + '`' for i in role.members])
            if len(text) > 3170:
                text = ", ".join(
                    (text[0:3170]).split(',')[:-1]) + ', And more...'
        else:
            text = '0 Members'
        embed = discord.Embed(
            color=easyembed.getcolor(ctx),
            title=f'Members of the role "{role.name}"',
            description=f'Total `{len(role.members)}`.\n{text}')
        await ctx.send(embed=embed)

    @commands.command()
    async def roleinfo(self, ctx, role: discord.Role):
        embed = discord.Embed(color=easyembed.getcolor(ctx),
                                title=f'Information about "{role.name}"')
        embed.add_field(name='ID and Name',
                        value=f'`{role.id}` | `{role.name}`',
                        inline=False)
        embed.add_field(name='Created at',
                        value=role.created_at,
                        inline=False)
        embed.add_field(name='Mentionable', value=role.mentionable)
        embed.add_field(name='Postition', value=str(role.position))
        embed.add_field(name='Color HEX Code', value=str(role.color))
        embed.set_thumbnail(
            url=f"https://serux.pro/rendercolour?hex={str(role.color)[1:]}"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def emojiinfo(self, ctx, emo: discord.Emoji):
        embed = discord.Embed(color=easyembed.getcolor(ctx),
                                title="Emoji Information")
        embed.add_field(name='Emoji ID', value=emo.id, inline=True)
        embed.add_field(name='Name', value=emo.name, inline=True)
        embed.add_field(name='Created at',
                        value=emo.created_at,
                        inline=True)
        embed.add_field(name='Server it belongs to (Name and ID)',
                        value=f"{emo.guild} | {emo.guild.id}",
                        inline=False)
        embed.add_field(name='Available for use?',
                        value=emo.available,
                        inline=True)
        embed.add_field(name='URL',
                        value=f'[Click to open]({emo.url})',
                        inline=False)
        embed.set_thumbnail(url=emo.url)
        await ctx.send(embed=embed)

    @commands.command(usage=':emoji:')
    async def emoji(self, ctx, emo: discord.Emoji):
        embed = discord.Embed(color=easyembed.getcolor(ctx),
                                title='Enlarge emoji').set_image(url=emo.url)
        await ctx.send(embed=embed)

    @commands.command(description='Get information about the current server.')
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(color=easyembed.getcolor(ctx),
                              title=f'Information about the current server.')

        def field(n: str, v: str, i: bool = False):
            return embed.add_field(name=n, value=v, inline=i)

        field("Member count", guild.member_count)
        field("Created at", guild.created_at)
        field('Description', guild.description or 'No description.')
        field('Emoji limit, voice channel bitrate limit and filesize limit',
            f'{guild.emoji_limit} | \
            {round(0.001*guild.bitrate_limit)} kbps | \
            {round(0.000001*guild.filesize_limit)} Megabytes'
        )
        field('Icon URL', f"[Click here]({guild.icon_url})")
        field('ID', guild.id)
        field('Features', ", ".join([f'`{i}`' for i in guild.features]))
        field(
            "Boost level and the current amount of boosts",
            f'`{str(guild.premium_tier)}` | `{guild.premium_subscription_count}`'
        )
        field('Banner URL', guild.banner_url or 'No banner found.')
        if len(channels := ", ".join([i.mention
                                      for i in guild.channels])) >= 1024:
            channels = ', '.join(
                channels[0:950].split(',')[0:-1]) + ', and more...'
        field('Channels', channels)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)
    @commands.command(description='Enlarge the icon of the current server.')
    async def serveravatar(self, ctx):
        embed = discord.Embed(
            title=f'Server icon of {ctx.guild.name}',
            color = easyembed.getcolor(ctx)
        ).set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Information(bot))