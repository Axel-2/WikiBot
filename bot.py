import os

import discord
from discord.ext import commands
from pymongo import MongoClient

MONGO_URL = os.environ.get("MONGO_URL")
cluster = MongoClient(MONGO_URL)
db = cluster["Guilds"]
collection = db["langue"]


def prefix(bot, message):
    guil_id = message.guild.id
    myquerry = {"_id": guil_id, "prefix": {'$exists': True}}
    if collection.count_documents(myquerry) == 0:
        return "?"
    querry = {"_id": guil_id}
    guild_prefix = collection.find(querry)
    for result in guild_prefix:
        guild_prefix = result["prefix"]
    return guild_prefix


bot = commands.Bot(command_prefix=prefix, description="Bot Wikipedia")

# enlever help de base
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Bot prêt!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("?help"))


startup_extensions = [
    'cogs.wikicommand',
    'cogs.helpcommand',
    'cogs.admin', 'cogs.adminserv',
    'cogs.random',
    "cogs.donation",
    'cogs.error',
    "cogs.jetphotos",
    "cogs.listlang"
]

for cog in startup_extensions:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)

try:
    token = os.environ["token"]
    bot.run(token)
except KeyError:
    print("WikiBeta")
    token = os.environ.get("BETA_TOKEN")
    ouk = os.environ.get("MONGO_URL")
    bot.run(token)
