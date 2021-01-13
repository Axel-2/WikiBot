import discord
from discord.ext import commands


class Donate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def donate(self, ctx):
        await ctx.send("https://donate.wikimedia.org/")


def setup(bot):
    bot.add_cog(Donate(bot))
