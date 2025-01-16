from discord.ext import commands
from discord.ext.commands import Context
import discord
from cogs.voice.backend import VoiceBackend

# Constants used in this file
MEMBER_ONLY_MSG = "Command can only be used as a member of a server"
GUILD_ONLY_MSG = "Command can only be used in a guild"
VOICE_CHANNEL_REQ_MSG = "You need to be in a voice channel to use this command"

class VoiceCommands(commands.Cog):
    def __init__(self, bot, voice_backend: VoiceBackend = VoiceBackend()):
        self.bot: commands.Bot = bot
        self.backend = voice_backend


    @commands.hybrid_group(name="voice", description="Voice commands")
    async def voice(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Use `/voice play <url>`, `/voice pause`, etc.")


    @voice.command(description="Make the bot join voice channel")
    async def join(self, ctx: Context) -> None:
        if not isinstance(ctx.author, discord.Member):
            await ctx.send(MEMBER_ONLY_MSG)
            return
            
        author_member: discord.Member = ctx.author
        author_vc = author_member.voice.channel if author_member.voice else None
        guild = author_member.guild

        if author_vc is None:
            await ctx.send(VOICE_CHANNEL_REQ_MSG)
            return
        else:
            await self.backend.activate(guild, author_vc)

        await ctx.send(f"Joined {author_vc.name} voice channel!")

    @voice.command(description="Make the bot leave voice channel")
    async def leave(self, ctx: Context):
        if not isinstance(ctx.guild, discord.Guild):
            await ctx.send(GUILD_ONLY_MSG)
            return

        guild = ctx.guild
        status = await self.backend.deactivate(guild)
        if status:
            await ctx.send("Disconnected from voice channel")
        else:
            await ctx.send("Bot is not in any voice channel")


    @voice.command(description="Skip current track")
    async def skip(self, ctx: Context):
        if not isinstance(ctx.author, discord.Member):
            await ctx.send(MEMBER_ONLY_MSG)
            return

        author_member: discord.Member = ctx.author
        guild = author_member.guild

        now_playing_track = self.backend.get_guild_voice_state(guild).now_playing
        if now_playing_track:
            await ctx.send(f"Track \"**{now_playing_track.title}**\" skipped")
            self.backend.get_guild_voice_state(guild).skip()
        else:
            await ctx.send("No track is currently playing")

    @voice.command(description="See track queue")
    async def queue(self, ctx: Context):
        guild = ctx.guild
        if not isinstance(guild, discord.Guild):
            await ctx.send(GUILD_ONLY_MSG)
            return
            
        voice_state = self.backend.get_guild_voice_state(guild)
        queue = voice_state.queue

        embed = discord.Embed(title="Track Queue", color=discord.Color.blue())
        if not queue:
            embed.description = "No tracks in the queue"

        for i, track in enumerate(queue):
            title = track.title
            value = f"{i+1}. {title}"
            embed.add_field(name=f"Track {i+1}", value=value, inline=False)

        await ctx.send(embed=embed, ephemeral=True)

    @voice.command(description="See now playing")
    async def nowplaying(self, ctx: Context):
        guild = ctx.guild
        if not isinstance(guild, discord.Guild):
            await ctx.send(GUILD_ONLY_MSG)
            return

        voice_state = self.backend.get_guild_voice_state(guild)
        embed = discord.Embed(title="Now playing", color=discord.Color.blue())
        now_playing = voice_state.now_playing

        if now_playing is None:
            embed.description = "Nothing is currently playing"
        else:
            embed.description = f"Playing \"{now_playing.title}\""

        await ctx.send(embed=embed, ephemeral=True)

    @voice.group(name="add", description="Play audio")
    async def add(self, _):
        pass

    @add.command(description="Add audio from YouTube URL")
    async def url(self, ctx: Context, url: str) -> None:
        await self.discord_enqueue_audio_helper(ctx, url, True)

    @add.command(description="Add audio from a YouTube search query")
    async def search(self, ctx: Context, query: str):
        await self.discord_enqueue_audio_helper(ctx, query, False)

    @voice.command(description="Remove item from queue")
    async def remove(self, ctx: Context, track_num: int):
        guild = ctx.guild
        if not isinstance(guild, discord.Guild):
            await ctx.send(GUILD_ONLY_MSG)
            return

        voice_state = self.backend.get_guild_voice_state(guild)
        queue = voice_state.queue

        if track_num < 1 or track_num > len(queue):
            await ctx.send("Please enter a valid track number to remove from queue", ephemeral=True)

        removed_track = queue[track_num - 1]
        del queue[track_num - 1]

        embed = discord.Embed(title="Track removed", color=discord.Color.blue())
        embed.description = f"Track \"**{removed_track.title}**\" removed"
        await ctx.send(embed=embed)

    # Command helpers
    async def discord_enqueue_audio_helper(self, ctx: Context, query: str, url=False) -> None:
        await ctx.defer()

        if not isinstance(ctx.author, discord.Member):
            await ctx.send(MEMBER_ONLY_MSG)
            return

        author_member: discord.Member = ctx.author
        author_vc = author_member.voice.channel if author_member.voice else None
        if author_vc is None:
            await ctx.send(VOICE_CHANNEL_REQ_MSG)
            return

        guild = author_member.guild

        await self.backend.activate(guild, author_vc)
        voice_state = self.backend.get_guild_voice_state(guild)

        audio = self.backend.yt_dlp_search_and_enqueue(query, guild, url)
        if audio is None:
            await ctx.send("Failed to add audio to queue")
            return

        embed = discord.Embed(title=f"Track Queued:", color=discord.Color.blue())  # Embed with blue color
        embed.add_field(name="Title", value=audio.title, inline=False)

        voice_state.play()

        await ctx.send(embed=embed)
        
