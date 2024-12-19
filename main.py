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

@bot.command()
async def create_role(ctx, *role_name:str):
    guild = ctx.guild
    role_name = " ".join(role_name)
    try:
        if not role_name in [role.name for role in guild.roles]:
            await guild.create_role(name=role_name)
            await ctx.send(f"role `{role_name}` created!")
        else:
            await ctx.send(f"role `{role_name}` already exists!")
    except:
        await ctx.send(f"unable to create `{role_name}` :c")

bot.run(os.getenv('token'))