import discord
from discord.ext import commands
from random import choice
class fun(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
 
    @commands.command(name='die', help='This command returns a random last words')
    async def die(self, ctx):
        responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
        await ctx.send(choice(responses))
 
    @commands.command(name='credits', help='This command returns the credits')
    async def credits(self, ctx):
        await ctx.send('Made by `RK Coding`')
        await ctx.send('Thanks to `DiamondSlasher` for coming up with the idea')
        await ctx.send('Thanks to `KingSticky` for helping with the `?die` and `?creditz` command')
        await ctx.send ('Thans to `Aadit` for tweaking the main code a bit')
 
    @commands.command(name='creditz', help='This command returns the TRUE credits')
    async def creditz(self, ctx):
        await ctx.send('**No one but me, lozer!**')
    @commands.command(name="clearmessages")
    async def cls(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)    

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(fun(bot)) # add the cog to the bot           