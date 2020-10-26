import discord
from discord.ext import commands, tasks
import youtube_dl

client=commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("a intrat tata nelson!")

client.run(DISCORD_SECRET)
