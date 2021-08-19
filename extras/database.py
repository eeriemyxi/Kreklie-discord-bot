from deta import Deta
import os
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("discord").setLevel(logging.WARNING)
log = logging.info
deta = Deta(os.getenv('DATABASE_KEY'))
userdb = deta.Base('user_data')


class Database_Listener(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.checked = []
    @commands.Cog.listener()
    async def on_message(self, msg):
        if (userid:= msg.author.id in self.checked):
            return
        if (check:= Database().checkuser(msg, userdb)):
            self.checked.append(msg.author.id)

class Database:
    def __init__(self) -> None:
        self.getembedcolor = [i.strip() for i in os.getenv('DEFAULT_EMBED_COLOR').split(',')]

    def checkuser(self, ctx, db):
        self.userid = str(ctx.author.id)
        if not (cache := db.get(self.userid)):
            db.put(data={
                'settings': {
                    'embedcolor': self.getembedcolor,
                    'ghostping': 'on'
                }
            },
                   key=self.userid)
            return True
        elif cache.get('settings'):
            if not cache.get('embedcolor'):
                db.update(updates={'settings.embedcolor': self.getembedcolor},
                          key=self.userid)
            if not cache.get('ghostping'):
                db.update(updates={'settings.ghostping': 'on'},
                          key=self.userid)
            return True
        else:
            db.put(
                {
                    "settings": {
                        'embedcolor': self.getembedcolor,
                        'ghostping': 'on'
                    }
                },
                key=self.userid)
            return True