import discord
from discord.ext import commands
from discord.ext.commands import Context
from collections import deque
from typing import Dict
from cogs.voice.voice_state import VoiceState
from cogs.voice.audio_item import Audio
from cogs.voice.helpers import yt_dlp_search

class VoiceBackend(commands.Cog):
    def __init__(self):
        self.guild_voice_states: Dict[discord.Guild, VoiceState] = {}

    def get_guild_voice_state(self, guild: discord.Guild) -> VoiceState:
        guild_voice_state = None
        if guild in self.guild_voice_states:
            guild_voice_state =  self.guild_voice_states[guild]
        else:
            guild_voice_state = VoiceState()
            self.guild_voice_states[guild] = guild_voice_state

        return guild_voice_state

    def get_guild_queue(self, guild: discord.Guild) -> deque[Audio]:
        return self.get_guild_voice_state(guild).queue


    def yt_dlp_search_and_enqueue(self, query: str, guild: discord.Guild, url: bool=False) -> Audio | None:
        info = yt_dlp_search(query, url)
        if info is None:
            return None

        audio = Audio(info['title'], info['url'])
        self.get_guild_queue(guild).append(audio)
        return audio

    async def activate(self, guild: discord.Guild, voice_channel: discord.VoiceChannel | discord.StageChannel) -> None:
        voice_state = self.get_guild_voice_state(guild)
        await voice_state.activate(voice_channel)

    async def deactivate(self, guild: discord.Guild) -> bool:
        voice_state = self.get_guild_voice_state(guild)
        return await voice_state.deactivate()
