import os
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('ready')

@client.event
async def on_message(message):
    if message.content.startswith('hello'):
        await message.channel.send('Hello')


client.run(os.getenv('token'))