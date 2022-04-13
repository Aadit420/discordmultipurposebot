import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
import asyncio
from discord.utils import get
import os
from random import choice
youtube_dl.utils.bug_reports_message = lambda: ''
from neuralintents import GenericAssistant
import nltk
nltk.download('omw-1.4')
load_dotenv()
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
 
ffmpeg_options = {
    'options': '-vn'
}
 
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
 
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
 
        self.data = data
 
        self.title = data.get('title')
        self.url = data.get('url')
 
    @classmethod
    async def from_url(cls, url, *, loop=True, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
 
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
 
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
 
def is_connected(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_connected()
 
def is_playing(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_playing()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='?', intents=intents)
 
status = ['Jamming out to music!', 'Eating!', 'Sleeping!', 'Call Of Duty:Mobile']
queue = []
loop = False

chatbot = GenericAssistant("intents.json")
chatbot.train_model()
chatbot.save_model()


@client.event
async def on_ready():
    change_status.start()
    print('Logged on as {0}!'.format(client.user))

@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.listen('on_message')
async def printtoconsole(message):
    print(f"message from {message.author}: {message.content}")
    if message.content.startswith("pythonbot"):
        response = chatbot.request(message.content[7:])
        await message.channel.send(response)



 
@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
 
    else:
        channel = ctx.message.author.voice.channel
 
    await channel.connect()
 
@client.command(name='leave', help='This command stops the music and makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
 
@client.command(name='loop', help='This command toggles loop mode')
async def loop_(ctx):
    global loop
 
    if loop:
        await ctx.send('Loop mode is now `False!`')
        loop = False
 
    else: 
        await ctx.send('Loop mode is now `True!`')
        loop = True
 
@client.command(name='play', help='This command plays music')
async def play(ctx, *, url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    global queue
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return    
    elif len(queue) == 0:
           queue.append(url)   
    else:
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        except: 
            pass

    
    while queue:
        try:
            while voice_channel.is_playing() or voice_channel.is_paused():
                await asyncio.sleep(1)
                pass

        except AttributeError:
            pass

        
        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(queue[0], loop=client.loop)
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                
                if loop:
                    queue.append(queue[0])

                del(queue[0])
                
            await ctx.send('**Now playing:** {}'.format(player.title))

        except:
            break

@client.command(name='volume', help='This command changes the bots volume')
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("Not connected to a voice channel.")
    
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")

 
@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    await ctx.send("Paused!")
    voice_channel.pause()
 
@client.command(name='resume', help='This command resumes the song!', aliases=['re'])
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    await ctx.send("Resumed!") 
    voice_channel.resume()
 
@client.command(name='stop', help='This command stops the song!', aliases=['s'])
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
 
    voice_channel.stop()
 
@client.command(name='queue', aliases=["q"], help='This helps to place a song on queue (queue song before using ```?play```')
async def queue_(ctx, *, url):
    global queue
 
    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')
 
@client.command(name='remove', aliases=['r'])
async def remove(ctx, number):
    global queue
 
    try:
        del(queue[int(number)-1])
        await ctx.send(f'Your queue is now `{queue}!`')
 
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')
 
@client.command(name='view', help='This command shows the queue', aliases=['v'])
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')
 
@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))
 
@client.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
    global queue
    voice = get(client.voice_clients, guild=ctx.guild)
 
    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=client.loop)
            voice.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send('Skipped, **Now playing:** {}'.format(player.title))
    else:
        print("No music playing")
        await ctx.send("No music playing failed")
 
cogs_list = [
    'greetings',
    'math',
    'fun'
]

for cog in cogs_list:
    client.load_extension(f'cogs.{cog}')
 
client.run(os.getenv("TOKEN"))