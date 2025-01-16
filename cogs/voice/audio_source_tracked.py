import discord

class AudioSourceTracked(discord.AudioSource):
    def __init__(self, source):
        self._source = source
        self.count_20ms = 0
    def read(self) -> bytes:
        data = self._source.read()
        if data:
            self.count_20ms += 1
        return data

    @property
    def progress(self) -> int:
        return self.count_20ms * 20
