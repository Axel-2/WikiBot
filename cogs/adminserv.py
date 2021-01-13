# Imports
from discord.ext import commands
from pymongo import MongoClient
import os

MONGO_URL = os.environ.get("MONGO_URL")
cluster = MongoClient(MONGO_URL)
db = cluster["Guilds"]
collection = db["langue"]


# Client commands
class AdminServ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 562297628700835871

    # Commands
    @commands.command()
    async def setprefix(self, ctx, prefix):
        guild_id = ctx.message.guild.id
        myquery = {"_id": guild_id}
        try:
            if collection.count_documents(myquery) == 0:
                post = {"_id": guild_id, "prefix": prefix}
                collection.insert_one(post)
            else:
                query = {"_id": guild_id}
                collection.find(query)
                collection.update_one({"_id": guild_id}, {"$set": {"prefix": prefix}})
            await ctx.send(f"Prefix is now {prefix}")
        except:
            await ctx.send("Error")

    @commands.command()
    async def setlang(self, ctx, lang):
        guild_id = ctx.message.guild.id
        if lang not in (
            "en",
            "fr",
            "es",
            "sv",
            "de",
            "nl",
            "no",
            "da",
            "nn",
            "af",
            "nds",
            "lb",
            "it",
            "pt",
            "ru",
        ):
            await ctx.send("Invalid ISO code. Check ?listlang.")
            return
        await ctx.send(f"The language is now {lang}.")
        myquery = {"_id": guild_id}
        if collection.count_documents(myquery) == 0:
            post = {"_id": guild_id, "lang": str(lang)}
            collection.insert_one(post)
        else:
            query = {"_id": guild_id}
            collection.find(query)
            collection.update_one({"_id": guild_id}, {"$set": {"lang": lang}})


def setup(bot):
    bot.add_cog(AdminServ(bot))
