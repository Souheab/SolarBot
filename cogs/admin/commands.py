from discord.ext import commands
from discord.ext.commands import Context
from consts import ADMIN_ID
import json

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def addmentionresponse(self, ctx: Context, response):
        if ctx.author.id != ADMIN_ID:
            await ctx.send("You do not have permission to use this command.")
            return
        self.bot.mention_responses.append(response)
        with open('./assets/mention_responses.json', 'w') as f:
            json.dump(self.bot.mention_responses, f)
        await ctx.send(f"Response: \"{response}\" added.")

    @commands.command(hidden=True)
    async def removementionresponse(self, ctx: Context, response):

        if ctx.author.id != ADMIN_ID:
            await ctx.send("You do not have permission to use this command.")
            return

        response_found = False
        updated_responses = []
        for r in self.bot.mention_responses:
            if r == response:
                response_found = True
            else:
                updated_responses.append(r)

        if not response_found:
            await ctx.send(f"Response: \"{response}\" not found.")
            return

        mention_responses = updated_responses
        self.bot.mention_responses = [r for r in mention_responses if r != response]
        with open('./assets/mention_responses.json', 'w') as f:
            json.dump(self.bot.mention_responses, f)
        await ctx.send(f"Response: \"{response}\" removed.")
