from discord.ext import commands
import requests
import discord
import datetime
from bs4 import BeautifulSoup

class Plane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def plane(self, ctx, plane):
        # base
        JETPHOTOS_URL = "https://www.jetphotos.com"

        # recuperer lien avion
        base_url = "https://www.jetphotos.com/photo/keyword/"
        recherche = base_url + plane
        page = requests.get(recherche)
        soup = BeautifulSoup(page.content, "html.parser")
        link_images = soup.find_all(class_="result__photoLink")
        text = link_images[0]
        plane_id = text.get("href")
        final_url = "https://www.jetphotos.com" + plane_id


        # recuperer page informations avion


        page = requests.get(final_url)
        soup = BeautifulSoup(page.content, "html.parser")
        list_link = []

        for ul_tag in soup.find_all("li", class_="list__item"):
            for span_tag in ul_tag.find_all("span"):
                for a_tag in span_tag.find_all("a"):
                    href = a_tag.get("href")
                    link = JETPHOTOS_URL + href
                    list_link.append(href)

        link_aircraft_info = JETPHOTOS_URL + list_link[1]

        # recuperer information avion
        page = requests.get(link_aircraft_info)
        soup = BeautifulSoup(page.content, "html.parser")
        infos = []

        for ul_tag in soup.find_all("ul", class_="list list--unstyled"):
            for li_tag in ul_tag.find_all("li", class_="list-item"):
                for span_tag in li_tag.find_all("span"):
                    strong_tag = span_tag.contents[0]
                    definition = str(strong_tag.text)
                    if len(span_tag.contents) > 1:
                        information = str(span_tag.contents[1])
                        infos.append({definition: information})


        # embed
        embed = discord.Embed(title=plane, description="Informations")
        embed.colour = discord.Colour.dark_blue()
        for dict in infos:
            for cle, valeur in dict.items():
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
        await ctx.send(final_url)



def setup(bot):
    bot.add_cog(Plane(bot))