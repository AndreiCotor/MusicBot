import discord
from discord.ext import commands, tasks
import youtube_dl
import os
from random import choice

youtube_dl.utils.bug_reports_message = lambda: ''

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
    'source_address': '0.0.0.0'
}

ffmpeg_options={
    'options': '-vn'
}

ytdl=youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

client=commands.Bot(command_prefix=".")
queue=[]

@client.event
async def on_ready():
    print("a intrat tata nelson!")

@client.command(name='ping', help='tie tata nelson cat de bine mere sony vayo')
async def ping(ctx):
    await ctx.send(f'**TIEEE TATA** 87 cu 87 cu 87 cu 87, odata de 4 ori 87 ii: {round(client.latency * 1000)}ms')

@client.command(name='credits', help='cine l-o facut pe tata nelson')
async def credits(ctx):
    await ctx.send('**LOL** nime, tata nelson valoare! 9 miloane 6 sute am in baie!')

@client.command(name='intra', help='vin voice')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("**MAAAAIIIIII** tu imi dai mie mare tzeapa? ma chemi pe voice si tu nu esti?")
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@client.command(name='baga', help='baga muzica valoroasa!')
async def add(ctx, url):
    global queue
    queue.append(url)
    await ctx.send(f'pune tata `{url}`, da cum sa nu puna')

@client.command(name='coada', help='ce ai bagat?')
async def queue(ctx):
    await ctx.send(f'bagam `{queue}`')

@client.command(name='iesi', help=':(((((((')
async def leave(ctx):
    voice_client=ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='pauza', help='muzica adevarata nu se opreste! tie tata')
async def stop(ctx):
    voice_channel=ctx.message.guild.voice_client
    voice_channel.stop()

@client.command(name='play', help='This command plays songs')
async def play(ctx):
    global queue
    voice_channel=ctx.message.guild.voice_client

    async with ctx.typing():
        player=await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('DACA SONY VAYO ATUNCI AM REZOLVAT SONY VAYO: %s' % e) if e else None)

    del(queue[0])

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

client.run(os.environ.get('DISCORD_SECRET'))
