import os
import discord
from deta import Deta

deta = Deta(os.getenv('DATABASE_KEY'))
db = deta.Base('user_data')


class easyembed(discord.Embed):
    default = (32, 34, 37)

    @classmethod
    def error(self, title, desc, ctx):
        id = str(ctx.author.id)
        check = db.get(id)
        if check and 'embedcolor' in check['settings']:
            ctx = check['settings']['embedcolor']
        else:
            ctx = self.default
        return self(title=title,
                    description=desc,
                    color=discord.Color.from_rgb(*(tuple(ctx))))
    @classmethod
    def unknown(self,ctx,user):
        id = str(ctx.author.id)
        check = db.get(id)
        if check and 'embedcolor' in check['settings']:
            ctx = check['settings']['embedcolor']
        else:
            ctx = self.default
        return self(title='Unknown error',
                    description=f'Please report it by typing <@{user.id}> report',
                    color=discord.Color.from_rgb(*(tuple(ctx))))
    @classmethod
    def simple(self, title, desc, ctx):
        id = str(ctx.author.id)
        check = db.get(id)
        if check and 'embedcolor' in check['settings']:
            ctx = check['settings']['embedcolor']
        else:
            ctx = self.default
        return self(title=title,
                    description=desc,
                    color=discord.Color.from_rgb(*(tuple(ctx))))
    @classmethod
    def getcolor(self, ctx):
        id = str(ctx.author.id)
        check = db.get(id)
        if check and 'embedcolor' in check['settings']:
            ctx = check['settings']['embedcolor']
        else:
            ctx = self.default
        return discord.Color.from_rgb(*(tuple(ctx)))