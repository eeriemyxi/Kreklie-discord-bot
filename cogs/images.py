import discord, os ; from discord.ext import commands
from extras.API_Requests import others; from extras.API_Requests import animals as animal_image; from extras.easy_embed import easyembed
class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group()
    async def animals(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)
    @animals.command(description = 'Shows a random image of a fox')
    async def fox(self, ctx):
        await ctx.send(embed = discord.Embed(color = easyembed.getcolor(ctx), title = 'Random image of a fox').set_image(url = animal_image.fox()))
    @animals.command(description = 'Shows a random image of a dog')
    async def dog(self, ctx):
        await ctx.send(embed = discord.Embed(color = easyembed.getcolor(ctx), title = 'Random image of a dog').set_image(url = animal_image.dog()))
    @animals.command(description = 'Shows a random image of a cat')
    async def cat(self, ctx):
        await ctx.send(embed = discord.Embed(color = easyembed.getcolor(ctx), title = 'Random image of a cat').set_image(url = animal_image.cat()))
    @commands.command(description = 'Random images of food dishes')
    async def foodporn(self, ctx):
        await ctx.send(embed = discord.Embed(color = easyembed.getcolor(ctx), title = 'Food porn').set_image(url = others.foodish()))
def setup(bot):
    bot.add_cog(Images(bot))