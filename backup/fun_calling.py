from discord.ext import commands
import discord, asyncio
class Calling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.callss = []
    @commands.command(description='Call someone by mentioning them or by giving their user ID.')
    async def call(self, ctx, user:discord.User = None):
        if not isinstance(ctx.channel, discord.channel.DMChannel): 
            await ctx.send('This command only works in DM.')
            return
        if not user:
            if len(self.calls) == 0: await ctx.author.send("Are you sure that you accepted someone's call?") ; return
            for couple_index, couple in enumerate(self.calls):
                if ctx.author.id in couple:
                    for item in couple:
                        user = self.bot.get_user(item)
                        await user.send('Call ended.')
                    del self.calls[couple_index]
                else:
                    await ctx.author.send("Are you sure that you accepted someone's call?")
            return
        else:
            def delete():
                for couple_index, couple in enumerate(self.calls):
                    if ctx.author.id in couple:
                        del self.calls[couple_index]
            if user.bot: await ctx.author.send("You're trying to call a bot.") ; return
            if user == ctx.author: await ctx.author.send("You're trying to call yourself.") ; return
            if ([user.id, ctx.author.id] in self.calls): await ctx.author.send("You're already in a call with someone.") ; return
            self.calls.append([user.id, ctx.author.id])
            await ctx.send('Calling...')
            def check(rec, rec_user):
                if rec_user.id == user.id and msg.id == rec.message.id and str(rec.emoji) in ('👍','👎') and rec_user.bot is False:
                    return True
                else: 
                    return False
            try:
                embed2 = discord.Embed(title=f'Someone called you! ({ctx.author.name})', description=f'Hello, {ctx.author} is trying to call you. React with the 👍 emoji to accept or 👎 to decline.')
                msg = await user.send(embed = embed2)
                await msg.add_reaction('👍') ; await msg.add_reaction('👎')
            except discord.Forbidden:
                await ctx.author.send("Can't send messages to that user. Either I don't share any mutual server with that user or the user has disabled DMs."); delete() ; return
            try:
                reaction, recuser = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                await user.send("Declined the call. You didn't answer in time.")
                await ctx.send("User didn't answer in time.")
                delete()
                return
            else:
                if not str(reaction.emoji) == '👍':
                    await ctx.author.send('User declined the call.')
                    await user.send('Declined the call successfully.')
                    delete()
                    return
                await user.send(f'Alright! say hello to {ctx.author.name}! do `.call` to end the call.')
                await ctx.author.send(f'Alright! say hello to {user.name}! do `.call` to end the call.')
                while True:
                    try:
                        if ([user.id, ctx.author.id] in self.calls) is False: return
                        def check2(checkuser):
                            return checkuser.author.id == ctx.author.id or checkuser.author.id == user.id and not ctx.author.bot or not user.bot
                        msg = await self.bot.wait_for('message',check=check2, timeout=120)
                        if msg.content.startswith('.call') and msg.author.id == self.client.user.id: pass
                        else:
                            if msg.author.id == user.id:
                                embed1 = discord.Embed(title=f'Message from {str(msg.author.name)}', description=f'{msg.content}')
                                await ctx.author.send(embed=embed1)
                            else:
                                embed3 = discord.Embed(title=f'Message from {str(user.name)}', description=f'{msg.content}')
                                await user.send(embed = embed3)
                    except asyncio.TimeoutError:
                        await user.send('Call ended because none of you two replied within 2 minutes.')
                        await ctx.send('Call ended because none of you two replied within 2 minutes.')
                        delete()
                        return



--------------------------------------


    @commands.command(
        usage="@User",
        description='Call someone by mentioning them or by giving their user ID.'
    )
    async def call(self, ctx, user: discord.User = None):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(
                embed=easyembed.error(title='DM only command.',
                                      desc='This command only works in DM.',
                                      ctx=ctx))
            return
        if not user:
            if len(self.calls) == 0:
                await ctx.author.send(embed=easyembed.error(
                    title="Error",
                    desc="Are you sure that you accepted someone's call?",
                    ctx=ctx))
                return
            for couple_index, couple in enumerate(self.calls):
                if ctx.author.id in couple:
                    for item in couple:
                        user = self.bot.get_user(item)
                        await user.send(
                            easyembed.error('Call ended',
                                            'I did it on request.',
                                            ctx=ctx))
                    del self.calls[couple_index]
                else:
                    await ctx.author.send(embed=easyembed.error(
                        title="Error",
                        desc="Are you sure that you accepted someone's call?",
                        ctx=ctx))

            return
        else:

            def delete():
                for couple_index, couple in enumerate(self.calls):
                    if ctx.author.id in couple:
                        del self.calls[couple_index]

            if user.bot:
                await ctx.author.send(embed=easyembed.error(
                    'Error', "You're trying to call a bot.", ctx))
                return
            if user == ctx.author:
                await ctx.author.send(embed=easyembed.error(
                    'Error', "You're trying to call yourself.", ctx))
                return
            if ([user.id, ctx.author.id] in self.calls):
                await ctx.author.send(embed=easyembed.error(
                    'Error', "You're already in a call with someone else.",
                    ctx))
                return
            self.calls.append([user.id, ctx.author.id])
            await ctx.send(embed=discord.Embed(color=easyembed.getcolor(ctx),
                                               title='Calling...'))

            def check(rec, rec_user):
                if rec_user.id == user.id and msg.id == rec.message.id and str(
                        rec.emoji) in ('👍', '👎') and rec_user.bot is False:
                    return True
                else:
                    return False

            try:
                embed2 = discord.Embed(
                    color=easyembed.getcolor(ctx),
                    title=f'Someone called you! ({ctx.author.name})',
                    description=
                    f'Hello, {ctx.author} is trying to call you. React with the 👍 emoji to accept or 👎 to decline.'
                )
                msg = await user.send(embed=embed2)
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')
            except discord.Forbidden:
                await ctx.author.send(embed=easyembed.error(
                    "Unable to send",
                    "Can't send messages to that user. Either I don't share any mutual server with that user or the user has disabled DMs.",
                    ctx))
                delete()
                return
            try:
                reaction, recuser = await self.bot.wait_for('reaction_add',
                                                            check=check,
                                                            timeout=60)
            except asyncio.TimeoutError:
                await user.send(embed=easyembed.error(
                    'Call declined',
                    "Declined the call. You didn't answer in time.", ctx))
                await ctx.send(embed=easyembed.error(
                    'Call declined', "User didn't answer in time.", ctx))
                delete()
                return
            else:
                if not str(reaction.emoji) == '👍':
                    await ctx.author.send(embed=easyembed.simple(
                        'Call declined', 'They declined the call.', ctx))
                    await user.send(embed=discord.Embed(title='Declined.'))
                    delete()
                    return
                await user.send(embed=easyembed.simple(
                    'Call accepted',
                    f'Say hello to {ctx.author.name}! type `.call` to end the call.',
                    ctx))
                await ctx.author.send(embed=easyembed.simple(
                    'Call accepted',
                    f'Say hello to {user.name}! type `.call` to end the call.',
                    ctx))
                while True:
                    try:
                        if ([user.id, ctx.author.id] in self.calls) is False:
                            return

                        def check2(checkuser):
                            return checkuser.author.id == ctx.author.id or checkuser.author.id == user.id and not ctx.author.bot or not user.bot

                        msg = await self.bot.wait_for('message',
                                                      check=check2,
                                                      timeout=120)
                        if msg.content.startswith(
                                '.call'
                        ) and msg.author.id == self.client.user.id:
                            pass
                        else:
                            if msg.author.id == user.id:
                                embed1 = discord.Embed(
                                    color=easyembed.getcolor(ctx),
                                    title=
                                    f'Message from {str(msg.author.name)}',
                                    description=f'{msg.content}')
                                await ctx.author.send(embed=embed1)
                            else:
                                embed3 = discord.Embed(
                                    color=easyembed.getcolor(ctx),
                                    title=f'Message from {str(user.name)}',
                                    description=f'{msg.content}')
                                await user.send(embed=embed3)
                    except asyncio.TimeoutError:
                        for user in (ctx, user):
                            await user.send(embed=easyembed.simple(
                                'Call ended',
                                'None of you two replied within 2 minutes.',
                                ctx))
                        delete()
                        return