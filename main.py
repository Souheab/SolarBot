from typing import List
import discord
import os
import json
import random
from dotenv import load_dotenv
from discord.ext import commands
from cogs.admin.commands import AdminCommands
from cogs.image.commands import ImageCommands
from cogs.voice.commands import VoiceCommands
from cogs.general.commands import GeneralCommands
from consts import BOT_MENTION

load_dotenv()
discord.opus.load_opus("./libs/libopus.so.0.10.1")

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open('./assets/mention_responses.json', 'r') as f:
            self.mention_responses: List[str] = json.load(f)

        
    async def on_ready(self):
        print('Logged on as', self.user)
        for guild in self.guilds:
            print(f'Connected to guild: {guild.name} (id: {guild.id})')
        await bot.add_cog(VoiceCommands(bot))
        await bot.add_cog(GeneralCommands(bot))
        await bot.add_cog(AdminCommands(bot))
        await bot.add_cog(ImageCommands(bot))
        await bot.change_presence(activity=discord.Game(name="with your feelings 😏"))
        await bot.change_presence(status=discord.Status.online)
        await bot.tree.sync()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == BOT_MENTION:
            await message.channel.send(random.choice(self.mention_responses))
            
        await self.process_commands(message)

intents = discord.Intents.default()
intents.message_content = True
bot = MyBot(command_prefix=">", intents=intents)

token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    bot.run(token)
else:
    print("No token found in .env file.")
