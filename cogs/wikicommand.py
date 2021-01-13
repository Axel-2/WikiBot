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


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wiki(self, ctx, *recherche):
        # CHECKS
        def checkEmoji(reaction, user):
            return ctx.message.author == user and message_react.id == reaction.message.id

        def checkmessage(m):
            return m.author == author


        author = ctx.author
        guild_id = ctx.message.guild.id

        # DATABASE
        myquery = {"_id": guild_id, "lang": {'$exists': True}}
        if collection.count_documents(myquery) == 0:
            wikipedia.set_lang("en")
        else:
            query = {"_id": guild_id}
            guil_lang = collection.find(query)
            for result in guil_lang:
                lang = result["lang"]
                wikipedia.set_lang(lang)


        # FUNCTIONS
        async def printChoice(choice):

            page = wikipedia.WikipediaPage(choice)
            image_list = wikipedia.wikipedia.WikipediaPage(choice).images
            image = image_list[0]

            embed = discord.Embed(
                title=f"**{page.title}**",
                url=page.url,
                description=page.summary[0:1500] + "..."
            )
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/"
                    "commons/thumb/a/a7/Wikipedia_logo_v3.svg/1024px-Wikipedia_logo_v3.svg.png")
            embed.set_image(url=image)
            embed.colour = discord.Colour.dark_blue()
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(
                text="Asked by " + author.name,
                icon_url="https://image.flaticon.com/icons/png/512/48/48927.png"
            )

            await ctx.send(embed=embed)

        async def clear(amount=1):

            await ctx.channel.purge(limit=amount)

        async def twos_r():
            amount = 4
            await add_emojis(2)
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=checkEmoji)
            if reaction.emoji == "1️⃣":
                choix = 1
            elif reaction.emoji == "2️⃣":
                choix = 2
            elif reaction.emoji == "❌":
                await clear(amount)
                return
            else:
                await ctx.send("Bad emoji")
                return
            await clear(amount)
            choix = result[choix - 1]
            await printChoice(choice=choix)

        async def three_r():
            amount = 5
            await add_emojis(3)
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=checkEmoji)
            if reaction.emoji == "1️⃣":
                choice = 1
            elif reaction.emoji == "2️⃣":
                choice = 2
            elif reaction.emoji == "3️⃣":
                choice = 3
            elif reaction.emoji == "❌":
                await clear(amount)
                return
            else:
                await ctx.send("Wrong emoji")
                return
            await clear(amount)
            choice = result[choice - 1]
            try:
                await printChoice(choice=choice)
            except wikipedia.DisambiguationError as e:
                print(e.options)

        async def add_emojis(nb_emojis):
            emojis = ["1️⃣", "2️⃣", "3️⃣"]
            if nb_emojis == 3:
                for emoji in emojis:
                    await message_react.add_reaction(emoji)
                await message_react.add_reaction("❌")
            else:
                for emoji in emojis[0:1]:
                    await message_react.add_reaction(emoji)
                await message_react.add_reaction("❌")

        # FIND RESULT
        result = wikipedia.search(recherche, 3)

        # vérifier si il y 0 ou seulement 1 un résultat et casser la boucle
        if len(result) == 0:
            await ctx.send("No results. Try another search.")
            return

        elif len(result) == 1:
            await clear()

            await printChoice(result[0])
            return

        # PRINT RESULTS
        num = 1

        for i in result:
            await ctx.send(f"{num}. **{i}**")
            num += 1

        # MESSAGE FOR CHOOSE ARTICLE
        message_react = await ctx.send("Which article do you want to read ?")

        # HOW MANY EMOJIS
        if len(result) == 3:
            await three_r()
        elif len(result) == 2:
            await twos_r()


def setup(bot):
    bot.add_cog(Wiki(bot))
