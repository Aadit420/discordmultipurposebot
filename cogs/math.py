import discord
from discord.ext import commands

class mathe(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
    
    @commands.command(decription="to add 2 numbers")
    async def add(self, ctx, a :int, b:int):
        await ctx.send(a + b )

    @commands.command(description="to subtract a number")
    async def sub(self, ctx, a: int, b: int):
        await ctx.send(a - b)     

    @commands.command(description="to multiply a number")
    async def mul(self, ctx, a: int, b: int):
        await ctx.send(a * b)

    @commands.command(description="divide a number")
    async def div(self, ctx, a: int, b: int):
        await ctx.send(a / b)    

    @commands.command(description="to power a number")
    async def power(self, ctx, a: int, b: int):
        await ctx.send(a ** b)

    @commands.command(description="to square a number")
    async def root(self, ctx, a: int, b: int):
        await ctx.send(a ** 1/b)
    #@commands.command(description="it's a random number generator!")
    #async def random(ctx, a: int,b: int):
    #    await ctx.send(random.randint(a, b))     

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(mathe(bot)) # add the cog to the bot            