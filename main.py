import os
import redis
import discord
from datetime import datetime
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.polls = True

bot = commands.Bot(command_prefix='~', intents=intents)
redis_client = redis.Redis(host=os.getenv("redis_host"), port=os.getenv("redis_port"), decode_responses=True, username=os.getenv("redis_username"), password=os.getenv("redis_password"))

@bot.event
async def on_ready():
    check_reminder.start()
    print('ready')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
@commands.has_guild_permissions(administrator=True)
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


#roles
@bot.command()
async def role(ctx, *role_name:str):
    role_name = " ".join(role_name)
    try:
        if role_name in [role.name for role in ctx.guild.roles]:
            if not role_name in [role.name for role in ctx.author.roles]:
                await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, name=role_name), reason="set_role command initiated by user")
                await ctx.send(f"role `{role_name}` is now assigned to you!")
            else:
                await ctx.send(f"role `{role_name}` has already been assigned to you!")
        else:
            await ctx.send(f"role `{role_name}` does not exist! (you can create it by calling ~create_role [role name])")
    except:
        await ctx.send(f"unable to set role `{role_name}` for some reason :c")


@bot.command()
async def remove_role(ctx, *role_name:str):
    role_name = " ".join(role_name)
    try:
        if role_name in [role.name for role in ctx.guild.roles]:
            if role_name in [role.name for role in ctx.author.roles]:
                await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, name=role_name), reason="set_role command initiated by user")
                await ctx.send(f"role `{role_name}` is now removed from you!")
            else:
                await ctx.send(f"you do not have the role `{role_name}`!")
        else:
            await ctx.send(f"role `{role_name}` does not exist!")
    except:
        await ctx.send(f"unable to remove role `{role_name}` for some reason :c")

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def delete_role(ctx, *role_name:str):
    role_name = " ".join(role_name)
    try:
        if role_name in [role.name for role in ctx.guild.roles]:
            role = discord.utils.get(ctx.author.guild.roles, name=role_name)
            await role.delete()
            await ctx.send(f"role `{role_name}` has been deleted!")
    except:
        await ctx.send(f"unable to delete the role `{role_name}` :c")


#reminders
@tasks.loop(seconds=10)
async def check_reminder():
    channel = await bot.fetch_channel(os.getenv('reminder_channel_id'))
    now = datetime.now()
    date = now.strftime('%d-%m-%Y')
    time = now.strftime('%H%M')
    key = set_reminder_key(date, time)
    reminder = redis_client.hgetall(key)
    print(f"{key}\n{reminder}")
    if(reminder):
        await channel.send(reminder['reminder'])
        redis_client.delete(key)

@bot.command()
async def reminder(ctx, *reminder:str):
    try:
        if len(reminder) < 3:
            await ctx.send('please use the proper format')
        else:
            reminder_date = reminder[0]
            reminder_time = reminder[1]
            reminder = " ".join(reminder[2:])
            if redis_client.hset(set_reminder_key(reminder_date, reminder_time), mapping={'reminder_date': reminder_date, 'reminder_time': reminder_time, 'reminder': reminder}):
                await ctx.send("reminder set")
            else:
                await ctx.send("failed to set reminder :c")
    except:
        await ctx.send("unable to set reminder :c")


def set_reminder_key(date, time):
    return f"reminder_{date}_{time}"

bot.run(os.getenv('token'))