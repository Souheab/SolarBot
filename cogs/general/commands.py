from discord.ext import commands
from consts import ADMIN_ID

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(description="Pong!")
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.hybrid_command(description="whoami 🧐")
    async def whoami(self, ctx):
        if ctx.author.id == ADMIN_ID:
            await ctx.send(f"You are my creator, <@{ADMIN_ID}>")
        else:
            await ctx.send(f"Hi <@{ctx.author.id}>")
