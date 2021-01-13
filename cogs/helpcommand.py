import datetime
import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):

        commandes = [
                {"?help": "The help command."},
                {"?wiki []": "The search command."},
                {"?donate": "Link to the Wikipedia donate page."},
                {"?setprefix []": "Change prefix."},
                {"?setlang []": "Change language."},
                {"?listlang": "List of availables languages."},
                {"?random": "Random Wikpedia article."}
            ]


        embed = discord.Embed(title="Help", description="Command list")
        embed.colour = discord.Colour.dark_blue()

        for command in commandes:
            for key, value in command.items():
                embed.add_field(name=key, value=value, inline=True)

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
    bot.add_cog(Help(bot))
