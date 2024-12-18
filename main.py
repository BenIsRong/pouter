import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.polls = True

bot = commands.Bot(command_prefix='~', intents=intents)

@bot.event
async def on_ready():
    print('ready')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(os.getenv('token'))