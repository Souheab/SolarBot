import discord
from discord.ui import View, Button

class PaginatorImageSearchView(View):
    def __init__(self, ctx, results):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.results = results
        self.current_page = 0

    async def update_embed(self, interaction):
        embed = self.create_embed(self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self, page):
        result = self.results[page]
        embed = discord.Embed(
            title=result["title"],
            description="Image search",
            color=discord.Color.blue(),
            url=result["image"]["contextLink"]
        )
        embed.set_image(url=result["link"])
        embed.set_footer(text=f"Page {page + 1} of {len(self.results)}")
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, _: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, _: Button):
        if self.current_page < len(self.results) - 1:
            self.current_page += 1
            await self.update_embed(interaction)
