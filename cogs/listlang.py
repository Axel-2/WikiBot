import datetime
import discord
from discord.ext import commands


class ListLang(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listlang(self, ctx):
        languages = [
            {"en": "English"},
            {"fr": "French"},
            {"es": "Spanish"},
            {"sv": "Swedish"},
            {"de": "German"},
            {"nl": "Dutch"},
            {"no": "Norwegian"},
            {"da": "Danish"},
            {"nn": "Norwegian Nynorsk"},
            {"af": "Afrikaans"},
            {"lb": "Luxembourgish"},
            {"it": "Italian"},
            {"pt": "Portuguese"},
            {"ru": "Russian"},
            ]


        embed = discord.Embed(title="List of availables languages", description="List of availables languages")
        embed.colour = discord.Colour.dark_blue()

        for language in languages:
            for cle, valeur in language.items():
                embed.add_field(name=cle, value=valeur, inline=True)

        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/"
                "Wikipedia_logo_v3.svg/1024px-Wikipedia_logo_v3.svg.png")
        embed.set_footer(
            text="Asked by " + ctx.author.name,
            icon_url="https://image.flaticon.com/icons/png/512/48/48927.png"
        )
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ListLang(bot))
