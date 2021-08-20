import os
import discord
from deta import Deta
from cogs.database import Database

deta = Deta(os.getenv('DATABASE_KEY'))
db = deta.Base('user_data')


class easyembed(discord.Embed):
    default = Database().getembedcolor

    @classmethod
    def error(self, title, desc, ctx):
        id = str(ctx.author.id)
        color = db.get(id)['settings']['embedcolor']
        return self(title=title,
                    description=desc,
                    color=discord.Color.from_rgb(*(tuple(color))))

    @classmethod
    def unknown(self, ctx, user):
        id = str(ctx.author.id)
        color = db.get(id)['settings']['embedcolor']
        return self(
            title='Unknown error',
            description=f'Please report it by typing <@{user.id}> report',
            color=discord.Color.from_rgb(*(tuple(color))))

    @classmethod
    def simple(self, title, desc, ctx):
        id = str(ctx.author.id)
        color = db.get(id)['settings']['embedcolor']
        return self(title=title,
                    description=desc,
                    color=discord.Color.from_rgb(*(tuple(color))))

    @classmethod
    def getcolor(self, ctx):
        id = str(ctx.author.id)
        color = db.get(id)['settings']['embedcolor']
        return discord.Color.from_rgb(*(tuple(color)))