import os
import redis
import discord
from datetime import datetime
from pymongo import MongoClient
from discord.ext import commands, tasks
from pymongo.server_api import ServerApi

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.polls = True

bot = commands.Bot(command_prefix='~', intents=intents)
client = MongoClient(f'mongodb+srv://pouter:{os.getenv("mongo_password")}@{os.getenv("mongo_host")}/?retryWrites=true&w=majority&appName=pouter', server_api=ServerApi('1'))

@bot.event
async def on_ready():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        check_reminder.start()
        print('ready')
    except Exception as e:
        print(e)

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
@tasks.loop(seconds=20)
async def check_reminder():
    channel = await bot.fetch_channel(os.getenv('reminder_channel_id'))
    now = datetime.now()
    date = now.strftime('%d-%m-%Y')
    time = now.strftime('%H%M')
    db = client["pouter"]
    collection = db["reminder"]
    results = [reminder for reminder in collection.find({"reminder_date": date, "reminder_time": time})]
    for result in results:
        await channel.send(result["reminder"])
    collection.delete_many({"reminder_date": date, "reminder_time": time})

@bot.command()
async def reminder(ctx, *reminder:str):
    db = client["pouter"]
    collection = db["reminder"]
    try:
        if len(reminder) < 3:
            await ctx.send('please use the proper format!')
        else:
            reminder_date = reminder[0]
            reminder_time = reminder[1]
            reminder = " ".join(reminder[2:])
            result = collection.insert_one({
                "reminder_date": reminder_date,
                "reminder_time": str(reminder_time),
                "author": {
                    "id": ctx.author.id,
                    "name": ctx.author.name,
                },
                "reminder": reminder
            })
            if(result):
                await ctx.send(f"the reminder has been set on {reminder_date}, {reminder_time}")
            else:
                await ctx.send("unable to set reminder :c")
    except:
        await ctx.send("unable to set reminder :c")

@bot.command()
async def remove_reminder(ctx, reminder_date:str, reminder_time:str):
    db = client["pouter"]
    collection = db["reminder"]
    try:
        if len([reminder for reminder in collection.find({"reminder_date": reminder_date, "reminder_time": reminder_time})]):
            collection.delete_one({"reminder_date": reminder_date, "reminder_time": reminder_time})
            await ctx.send("reminder removed!")
        else:
            await ctx.send("unable to find a reminder with the given date and time :c")
    except:
        await ctx.send("unable to remove reminder :c")

@bot.command()
async def update_reminder(ctx, *reminder:str):
    db = client["pouter"]
    collection = db["reminder"]
    try:
        if len(reminder) < 3:
            await ctx.send('please use the proper format!')
        else:
            reminder_date = reminder[0]
            reminder_time = reminder[1]
            reminder = " ".join(reminder[2:])
            result = collection.update_one({"reminder_date": reminder_date, "reminder_time": reminder_time},{
                "$set": {
                    "reminder": reminder
                }
            })
            if(result):
                await ctx.send("updated the reminder!")
            else:
                await ctx.send("unable to update the reminder :c")
    except:
        await ctx.send("unable to update the reminder :c")

@bot.command()
async def update_reminder_with_time(ctx, *reminder:str):
    db = client["pouter"]
    collection = db["reminder"]
    try:
        if len(reminder) < 5:
            await ctx.send('please use the proper format!')
        else:
            reminder_date = reminder[0]
            reminder_time = reminder[1]
            set_reminder_date = reminder[2]
            set_reminder_time = reminder[3]
            reminder = " ".join(reminder[4:])
            result = collection.update_one({"reminder_date": reminder_date, "reminder_time": reminder_time},{
                "$set": {
                    "reminder_date": set_reminder_date,
                    "reminder_time": str(set_reminder_time),
                    "reminder": reminder
                }
            })
            if(result):
                await ctx.send("updated the reminder!")
            else:
                await ctx.send("unable to update the reminder :c")
    except:
        await ctx.send("unable to update the reminder :c")


bot.run(os.getenv('token'))