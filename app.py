# app.py
import discord
from discord.ext import commands
from discord.ui import Button, View
import os
from dotenv import load_dotenv

from friend import STicTacToeView
from bot import ATicTacToeAIView

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class GameModeView(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(label="Play with Yourself", style=discord.ButtonStyle.primary, custom_id="self_play")
    async def self_play(self, interaction: discord.Interaction, button: Button):
        view = STicTacToeView(self.ctx.author, self.ctx.author)
        await interaction.response.send_message(f"Playing with yourself 😄\nYour turn {self.ctx.author.mention}", view=view)

    @discord.ui.button(label="Play with Friend", style=discord.ButtonStyle.success, custom_id="friend_play")
    async def friend_play(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Tag your friend using `!ttt @friend`", ephemeral=True)

    @discord.ui.button(label="Play with AI", style=discord.ButtonStyle.danger, custom_id="ai_play")
    async def ai_play(self, interaction: discord.Interaction, button: Button):
        view = ATicTacToeAIView(self.ctx.author)
        await interaction.response.send_message(f"Tic Tac Toe vs AI 🤖\nYou are ❌. Click a square to play.", view=view)

@bot.command()
async def ttt(ctx, opponent: discord.Member = None):
    if opponent:
        if opponent.bot:
            await ctx.send("You can't play against a bot!")
            return
        view = STicTacToeView(ctx.author, opponent)
        await ctx.send(f"{ctx.author.mention} vs {opponent.mention} – Tic Tac Toe!\n{ctx.author.mention}'s turn", view=view)
    else:
        view = GameModeView(ctx)
        await ctx.send("Choose a game mode:", view=view)

bot.run(TOKEN)
