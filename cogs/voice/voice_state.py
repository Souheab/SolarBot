from collections import deque
from cogs.voice.audio_item import Audio
import discord

class VoiceState():
    def __init__(self):
        self.playing = False
        self.queue: deque[Audio] = deque()
        self.active = False
        self.voice_client: discord.VoiceClient | None = None
        self.voice_channel: discord.VoiceChannel | discord.StageChannel | None = None
        self.player = None
        self.now_playing = None

    async def deactivate(self) -> bool:
        if not self.active:
            return False
        self.playing = False
        self.queue = deque()
        self.active = False
        if self.voice_client:
            await self.voice_client.disconnect(force=True)
            self.voice_client = None
            return True
        else:
            return False

    async def activate(self, voice_channel: discord.VoiceChannel | discord.StageChannel) -> discord.VoiceClient | None:
        if self.active:
            return self.voice_client
        self.playing = False
        self.queue = deque()
        self.active = True
        if self.voice_client and self.voice_channel == voice_channel:
            await self.voice_client.move_to(voice_channel)
        else:
            self.voice_client = await voice_channel.connect()
        self.voice_channel = voice_channel

        return self.voice_client

    def play(self):
        if not self.active or not self.voice_client or self.playing:
            return

        if not self.queue:
            return

        audio = self.queue.pop()
        self.player = discord.FFmpegPCMAudio(audio.url, before_options="-reconnect 1 -reconnect_streamed 1")
        self.playing = True

        def after_playing(_: Exception | None):
            self.playing = False
            if self.queue:
                self.play()

        self.voice_client.play(self.player, after=after_playing)
        self.now_playing = audio

    def skip(self) -> Audio | None:
        if not self.active or not self.voice_client or not self.playing:
            return

        # Note: running stop method runs after_playing callback immidieately
        self.voice_client.stop() 
        self.playing = False
