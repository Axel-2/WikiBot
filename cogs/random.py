# NE FONCTIONNE PAS


import datetime
import os
import discord
import wikipedia
from discord.ext import commands
from pymongo import MongoClient

MONGO_URL = os.environ.get("MONGO_URL")
cluster = MongoClient(MONGO_URL)
db = cluster["Guilds"]
collection = db["langue"]


class RandomCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx):
        author = ctx.author
        guild_id = ctx.message.guild.id
        myquery = {"_id": guild_id, "lang": {'$exists': True}}
        if collection.count_documents(myquery) == 0:
            wikipedia.set_lang("en")
        else:
            query = {"_id": guild_id}
            guil_lang = collection.find(query)
            for result in guil_lang:
                lang = result["lang"]
                wikipedia.set_lang(lang)

            random_page = wikipedia.random(pages=1)


        def checkmessage(m):
            return m.author == author

        async def print_choice(page_random):
            try:
                page = wikipedia.WikipediaPage(random_page)
            except:
                await ctx.send("Error.")
            # image_list = wikipedia.wikipedia.WikipediaPage(page).images
            # image = image_list[0]
            image_list = wikipedia.WikipediaPage(page_random).images
            image = image_list[0]

            embed = discord.Embed(
                title=f"**{page.title}**",
                description=page.summary[0:400],
                url=page.url
            )
            embed.set_image(url=image)
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/"
                    "commons/thumb/a/a7/Wikipedia_logo_v3.svg/1024px-Wikipedia_logo_v3.svg.png"
            )
            # embed.set_image(url=image)
            embed.colour = discord.Colour.dark_blue()
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(
                text="Asked by " + author.name,
                icon_url="https://image.flaticon.com/icons/png/512/48/48927.png"
            )

            await ctx.send(embed=embed)

        async def clear(amount=1):
            await ctx.channel.purge(limit=amount)

        await clear()
        await print_choice(random_page)


def setup(bot):
    bot.add_cog(RandomCommand(bot))
