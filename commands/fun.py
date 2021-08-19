from discord.ext import commands
import discord, shutil, random, os
import extras.API_Requests as api
import requests as fetch
import asyncio
from extras.easy_embed import easyembed
from deta import Deta

deta = Deta(os.getenv('DATABASE_KEY'))
shipdb = deta.Base('ship_data')


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.calls = []
    @commands.command(
        description=
        'Shows a random person that doesn\'t exist. Thanks to thispersondoesnotexist.com'
    )
    async def tpde(self, ctx):
        res = fetch.get('https://thispersondoesnotexist.com/image',
                        stream=True)
        number = random.randint(1, 100000)
        with open(f'{number}.jpg', 'wb') as i:
            shutil.copyfileobj(res.raw, i)
            res.raw.decode_content = True
            i.close()
        with open(f'{number}.jpg', 'rb') as i:
            await ctx.send(content='This person does not exist!',
                           file=discord.File(i, 'tpde.jpg'))
            i.close()
        os.remove(f'{number}.jpg')

    @commands.command(
        description=
        'Sends a random joke. By default it\'s set to safe mode. But can be switched by typing unsafe after "joke"'
    )
    async def joke(self, ctx, unsafe=None):
        if not unsafe:
            text = api.others.joke(safe=True)
        elif unsafe == 'unsafe':
            text = api.others.joke(safe=False)
        embed = discord.Embed(title=text)
        await ctx.send(embed=embed)

    @commands.group(description='Get random facts about animals.')
    async def fact(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=easyembed.error(
                'Invalid subcommand',
                'Please have a look at the message below.', ctx))
            await ctx.send_help('fact')

    @fact.group(description='Get random facts about dog')
    async def dog(self, ctx):
        await ctx.send(embed=discord.Embed(color=easyembed.getcolor(ctx),
                                           title=api.others.dog_facts()))

    @fact.group(description='Get random facts about cat')
    async def cat(self, ctx):
        await ctx.send(embed=discord.Embed(color=easyembed.getcolor(ctx),
                                           title=api.others.cat_facts()))

    @commands.command(usage='<text or mention> , <text or mention>',
                      description='Matchmaking.')
    async def ship(self, ctx, name1, name2, *, not_needed=None):
        def get_review(i: int):
            if i >= 100:
                return '**PERFECT!**'
            elif i >= 80:
                return '**ALMOST Perfect!**'
            elif i >= 60:
                return "**Cute!**"
            elif i >= 40:
                return "**Not bad...**"
            elif i >= 20:
                return "**I have no words to say...**"
            elif i < 20:
                return "**Bad...**"

        key = "".join([name1, name2])
        if data := shipdb.get(key):
            percent = data['value']
        else:
            percent = random.randint(0, 100)
            shipdb.put(data=percent, key=key)
        embed = discord.Embed(
            color=easyembed.getcolor(ctx),
            title=":heartpulse:  MATCHMAKING  :heartpulse:",
            description=
            f":small_red_triangle_down: {name1}\n:small_red_triangle: {name2}\n{percent}% {get_review(percent)}"
        )
        await ctx.send(embed=embed)

    @ship.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if error.param.name == 'name1':
                await ctx.send(embed=easyembed.error(
                    'Missing text argument',
                    'The first name to ship with is missing.', ctx))
            elif error.param.name == 'name2':
                await ctx.send(embed=easyembed.error(
                    'Missing text argument',
                    'The second name to ship with is missing.', ctx))
            else:
                await ctx.send(embed=easyembed.unknown(ctx, self.bot.user))

    @commands.command(
        usage='<@user>',
        description=
        'Hack someone by information collected from dark web. This is totally illegal and real hacking trick.'
    )
    async def hack(self, ctx, user: discord.User):
        if str(user.id) == str(os.getenv('OWNER_ID')):
            await ctx.send(
                embed=easyembed.simple('AHAHAAHA', 'YOU CANT HACK ME', ctx))
            return
        percent_seq = sorted(
            random.sample(list(range(1, 100)), random.randint(8, 15)))
        percent_seq.append(100)
        msg = await ctx.send(
            embed=easyembed.simple(f'Hacking {user.name}!',
                                   f'Current progress: {percent_seq[0]}%', ctx)
        )
        await asyncio.sleep(1.5)
        for i in percent_seq[1:]:
            await msg.edit(embed=easyembed.simple(
                f'Hacking {user.name}!', f'Current progress: {i}%', ctx))
            await asyncio.sleep(1.5)
        word_list = [
            'cockhead', '6969', '69', 'lord', 'gayhead', 'craphead', 'crapper',
            'crapboy', 'crap69', 'gaming', 'gaymer', 'jesus', 'gamingboy',
            'yoyo', 'pussy', 'cute', 'tranny', 'peasant'
        ]
        email = "".join(random.choices(word_list,k=2)) + str(
            random.randint(0000, 5000)) + random.choice([
                '@gmail.com', '@outlook.com', '@yahoo.com', '@hotmail.com',
                'mail.com'
            ])
        password = random.choice([
            'lord2921', 'gamingguy', 'gamer69pro', 'noobboy69', 'ilovemymom',
            'idrinkgamergirlwater'
        ]) + str(random.randint(0000, 50000))
        ipaddress = ".".join([str(random.randint(0, 255)) for i in range(4)])
        embed = discord.Embed(
            color=easyembed.getcolor(ctx),
            title=f'Successfully hacked {user.name}',
        )
        embed.add_field(name='E-Mail', value=email, inline=False)
        embed.add_field(name='Password', value=password, inline=False)
        embed.add_field(name='IP Address', value=ipaddress, inline=False)
        await msg.edit(embed=embed)
