from discord.ext import commands
from discord.ext.commands import Context
from cogs.image.backend.speech_bubble import create_speech_bubble
from cogs.image.backend.search.google_search import GoogleSearchAPI
from cogs.image.backend.search.views import PaginatorImageSearchView
from PIL import Image
from io import BytesIO
import discord
import requests
import os
from discord import app_commands

class ImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.google_search_api = GoogleSearchAPI(os.getenv("GOOGLE_SEARCH_API_KEY"),
                                    os.getenv("GOOGLE_IMAGE_SEARCH_SS_CSE_ID"))

        
    @commands.hybrid_group(name="image", description="Voice commands")
    async def image(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Use `/image speechbubble` etc.")


    @image.command(description="Adds a speech bubble effect to an uploaded image or an image from a URL.")
    @app_commands.describe(
        uploaded_image="An image file uploaded directly to the command.",
        image_url="A URL to an image to be processed."
    )
    async def speechbubble(self, ctx, uploaded_image: discord.Attachment | None = None, image_url: str | None = None):
        image = None

        if uploaded_image:
            image_bytes = await uploaded_image.read()
            image = Image.open(BytesIO(image_bytes))

        elif image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))

        if image:
            speechbubble = create_speech_bubble(image)
            with BytesIO() as image_binary:
                speechbubble.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

        else:
            await ctx.send("Valid image not provided")


    @image.command(description="Retrieves and displays the avatar of a specified user or yourself.")
    @app_commands.describe(user="The user whose avatar you want to retrieve.")
    async def avatar(slef, ctx: Context, user: discord.User | None = None):
        user_real = user or ctx.author

        if user_real.avatar:
            await ctx.send(user_real.avatar.url)
        else:
            await ctx.send("User has no avatar")

    @image.command(description="Searches Images")
    @app_commands.describe(query="The search query to use")
    async def search(self, ctx, query: str):
        image_results_list = self.google_search_api.search_get_image_list(query)

        view = PaginatorImageSearchView(ctx, image_results_list)
        embed = view.create_embed(view.current_page)
        await ctx.send(embed=embed, view=view)
