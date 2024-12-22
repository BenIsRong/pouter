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


bot.run(os.getenv('token'))