from discord.errors import Forbidden
from discord.ext import commands
import discord, asyncio, os
from discord.ext.commands.errors import CommandInvokeError
from udpy import AsyncUrbanClient, UrbanClient
from duckduckgo_search import ddg
from PyDictionary import PyDictionary
import py_expression_eval as calc
from deta import Deta
from extras.easy_embed import easyembed

deta = Deta(os.getenv('DATABASE_KEY'))
userdb = deta.Base('user_data')
guilddb = deta.Base('guild_data')


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Calculator')
    async def calc(self, ctx, equation):
        if not equation:
            await ctx.send(embed=easyembed.error(
                'Error',
                'You forgot that you have to enter something that I could calculate.',
                ctx))
            await ctx.send_help('calc')
        else:
            result = calc.Parser().parse(equation).evaluate({})
            await ctx.send(result)

    @commands.command(
        description=
        'Convert binary to text or text to binary. This is how it\'s done:\nTo convert binary to text do .binary decode [text here] and to convert text to binary change "decode" to "encode".'
    )
    async def binary(self, ctx, answer=None, *, code=None):
        if not answer:
            await ctx.send(embed=easyembed.error(
                'Missing argument.', 'You forgot to include codec.', ctx))
        if answer and not code:
            await ctx.send(embed=easyembed.error(
                'Codec error',
                'You forgot to include what you wanted to decode or encode.',
                ctx))
        else:
            if code is not None:
                answer = answer.lower()
                if answer in ('encode', 'decode'):
                    if answer == 'encode':
                        binary = ' '.join(
                            format(x, 'b') for x in bytearray(code, 'utf-8'))
                        await ctx.send(binary)
                    else:
                        try:
                            ascii_string = "".join([
                                chr(int(binary, 2))
                                for binary in code.split(" ")
                            ])
                        except Exception:
                            await ctx.send(embed=easyembed.error(
                                'Unable to decode',
                                'Sorry, something went wrong when I tried to decode it.',
                                ctx))
                        else:
                            await ctx.send(
                                easyembed.simple(title='Result',
                                                 desc=ascii_string,
                                                 ctx=ctx))
                else:
                    await ctx.send(embed=easyembed.error(
                        'Invalid value for argument',
                        'Codec argument can either be "encode" or "decode".',
                        ctx))

    @commands.command(description='Search the Oxford Dictionary.')
    async def oxford(self, ctx, keyword=None):
        print('e')
        if not keyword:
            await ctx.send(
                'You forgot to include which word you wanted to search.')
        else:
            pydict = PyDictionary()
            meaning = pydict.meaning(keyword)
            embed = discord.Embed(title='Search results')
            embed.set_footer(text='Oxford Dictionary Search')
            for m in meaning:
                embed.add_field(name=m,
                                value="\n".join(["- " + i
                                                 for i in meaning[m]]),
                                inline=False)
            await ctx.channel.send(embed=embed)

    @commands.command(description='Search something on Urban Dictionary.')
    async def urban(self, ctx, *, keyword=None):
        if not keyword:
            await ctx.send(easyembed.error('Error', 'Empty input.', ctx))

        def check(rect, usr):
            if usr.id == ctx.author.id:
                if rect.message.channel.id == ctx.channel.id:
                    if str(rect.emoji) in ('➡️', '⬅️'):
                        if not usr.bot:
                            return True
            else:
                return False

        d = UrbanClient().get_definition(keyword)
        i = 0
        if len(d) <= 0:
            await ctx.send(embed=discord.Embed(title='No definitions found.'))
            return
        embed = discord.Embed(
            title=f"Definition of {d[i].word}", description=d[i].definition
        ).set_footer(
            text=
            f"Upvotes: {d[i].upvotes}, Downvotes: {d[i].downvotes}, Definition No. {i+1}"
        )
        msg = await ctx.send(embed=embed)
        for emote in ('⬅️', '➡️'):
            await msg.add_reaction(emote)
        while True:
            try:
                rect, user = await self.bot.wait_for('reaction_add',
                                                     check=check,
                                                     timeout=60)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                return
            else:
                if str(rect.emoji) == '➡️':
                    i += 1
                    if i >= len(d) - 1:
                        await msg.edit(embed=discord.Embed(
                            title='No more definitions found.'))
                        await msg.clear_reactions()
                        return
                    else:
                        await msg.edit(embed=discord.Embed(
                            title=f"Definition of {d[i].word}",
                            description=d[i].definition
                        ).set_footer(
                            text=
                            f"Upvotes: {d[i].upvotes}, Downvotes: {d[i].downvotes}, Definition No. {i+1}"
                        ))
                        continue
                else:
                    if i <= 0: i = len(d) - 1
                    i -= 1
                    await msg.edit(embed=discord.Embed(
                        title=f"Definition of {d[i].word}",
                        description=d[i].definition
                    ).set_footer(
                        text=
                        f"Upvotes: {d[i].upvotes}, Downvotes: {d[i].downvotes}, Definition No. {i+1}"
                    ))
                    continue

    @urban.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            error = error.original
            if isinstance(error, Forbidden):
                await ctx.send(embed=discord.Embed(
                    title='Error',
                    description='I lack the permission to remove reactions.'))

    @commands.command(
        description='Shows 10 search results of DuckDuckGo Search Engine.')
    async def ddg(self, ctx, *, keyword):
        embed = discord.Embed(color=easyembed.getcolor(ctx),title='DuckDuckGo - Search results')
        if keyword:
            results = ddg(keyword, max_results=10)
            for result in results:
                embed.add_field(
                    name=f'{result["title"]}',
                    value=
                    f'**- - - [Click here to visit]({result["href"]}) - - -**\n{result["body"]}',
                    inline=False)
            await ctx.send(embed=embed)

    @commands.group(aliases=['stgs'],description='Turn off or on some unnecessary stuff.')
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help('settings')

    @settings.group(
        usage='<on | off>',
        description=
        'Turn off ghost pings. You will not get notified when someone mentions you and deletes the message but if you ghost ping someone, they won\'t get notified either.'
    )
    async def ghostping(self, ctx, bool_value):
        if bool_value.lower() in ('on', 'off'):
            bool_value = bool_value.lower()
            userid = str(ctx.author.id)
            userdb.update(key=str(userid),
                              updates={'settings.ghostping': bool_value})
            await ctx.send(embed=discord.Embed(
                color=easyembed.getcolor(ctx),
                title='Done!',
                description=f'Set ghost ping setting to `{bool_value}`.'))
        else:
            await ctx.send(
                easyembed.error(
                    title='Error',
                    desc=f'Invalid value "{bool_value}" for the argument.',
                    ctx=ctx))

    @settings.group(
        usage='<red> <green> <blue>',
        description=
        'Choose what the embed should be. This applies only to the commands you execute.'
    )
    async def embedcolor(self, ctx, r, g, b):
        try:
            r, g, b = int(r), int(g), int(b)
        except Exception:
            await ctx.send(embed=easyembed.error(
                'Error', 'Only numbers below 255 allowed.', ctx))
            return
        for i in (r, g, b):
            if i > 255:
                await ctx.send(embed=easyembed.error(
                    'Number value over 255',
                    f'RGB values can\'t be higher than 255.', ctx))
                return
        userid = str(ctx.author.id)
        userdb.update(updates={'settings.embedcolor':[r,g,b]},key = userid)
        await ctx.send(embed=discord.Embed(
            color=discord.Color.from_rgb(*(r, g, b)),
            title='Done!',
            description=
            f'Embed color has been changed to RGB color value `{r},{g},{b}`'))
def setup(bot):
    bot.add_cog(Utilities(bot))