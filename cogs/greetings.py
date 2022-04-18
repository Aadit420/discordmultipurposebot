import discord
from discord.ext import commands
from random import choice

class Greetings(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.command(name='hello', help='This command returns a random welcome message')
    async def hello(self, ctx):
        responses = ['***grumble*** Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi', '**Wasssuup!**']
        await ctx.send(choice(responses))

    @commands.command()
    async def goodbye(self, ctx):
        await ctx.send('Goodbye!')
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name='general')
        await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `?help` command for details!')
        await member.send('Welcome to the server!')
 
    @commands.Cog.listener()
    async def on_member_leave(member):
        channel = discord.utils.get(member.guild.channels, name='general')
        await channel.send(f"I'm so sorry {member.mention} had to leave.")
        await member.send("Don't leave!")
    @commands.command()
    async def invite(self,ctx):
        await ctx.send("https://discord.com/api/oauth2/authorize?client_id=760289979590770738&permissions=8&scope=bot%20applications.commands")
        async with ctx.typing():
             await ctx.send("help spread the bot to more servers!")
 

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Greetings(bot)) # add the cog to the bot