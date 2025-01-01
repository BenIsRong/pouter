<h1 align=center>Introduction</h1>

## What is pouter?
Pouter (stylized as `pouter`) simple Discord bot that helps manage your everyday tasks in your server. The goal of this bot is not to be some glamourous bot that can do lots and lots of things, but to do enough that the human element of a server is still kept as is.<br/>
Everything is done using [discord.py](https://github.com/Rapptz/discord.py), so please do check them out!

## Why is pouter?
Because I am very bored at home and I need something to do.

## How is pouter?
pouter is doing well! Although it is (clearly) still a work in progress, there is no set deadline for pouter. That being said, anyone is free to fork the project and create their own lil pouter!

<h1 align=center>Setup</h1>

## What do I need?
The following things are needed:
 - [Python (3.11 or above)](https://www.python.org/downloads/)
 - [MongoDB Atlas](https://www.mongodb.com/atlas)
 - [A Discord Bot called pouter](https://discordpy.readthedocs.io/en/stable/discord.html)

## How do I get started?
First things first! You have to set up your MongoDB stuff!
- Create the `pouter` database in the MongoDB cluster that you plan to use
- Create a collection called `reminders`

Once that is done, you can then do the following on the computer you plan to use pouter on:
- Fork/clone the repository to your computer
- Open Command Prompt
- cd to the path that the repository is at
- run `pip install -r requirements.txt`
- Using your favourite code editor, open the project
- Duplicate .env.example and rename it as .env
- add the following items to the .env file:

| item | value | where to get |
|--|--|--|
| token | bot token | [Discord Developer](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token) |
| reminder_channel_id | channel id of your reminder channel | right click the channel and select Copy Channel ID (make sure Developer Mode is enabled)|
| mongo_host | host url for mongodb | MongoDB Atlas |
| mongo_username | username for mongodb | MongoDB Atlas |
| mongo_password | password for mongodb | MongoDB Atlas |

Once all of that is done, you can do whatever you want to pouter! Just don't be mean to it, please...!
