from discord.ext import commands


class Guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == 562297628700835871

    @commands.command()
    async def guilds(self, ctx):
        async for guild in self.bot.fetch_guilds(limit=150):
            await ctx.send(guild.name)

    @commands.command()
    async def lenguilds(self, ctx):
        guilds = []
        async for guild in self.bot.fetch_guilds(limit=150):
            guilds.append(guild)
            await ctx.send(len(guilds))
            del guilds



def setup(bot):
    bot.add_cog(Guilds(bot))
