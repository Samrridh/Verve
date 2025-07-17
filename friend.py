# friend.py
import discord
from discord.ui import Button, View

class STicTacToeButton(Button):
    def __init__(self, row, col, parent_view):
        super().__init__(label="⬜", row=row)
        self.row = row
        self.col = col
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        if not self.parent_view.game_active:
            await interaction.response.send_message("Game has ended!", ephemeral=True)
            return

        player = self.parent_view.players[self.parent_view.turn]
        if interaction.user != player:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        symbol = "❌" if self.parent_view.turn == 0 else "⭕"
        self.label = symbol
        self.disabled = True
        self.style = discord.ButtonStyle.danger if symbol == "❌" else discord.ButtonStyle.primary
        self.parent_view.board[self.row][self.col] = symbol

        winner = self.parent_view.check_winner()
        if winner:
            self.parent_view.game_active = False
            await interaction.response.edit_message(content=f"{player.mention} wins!", view=self.parent_view)
        elif self.parent_view.is_draw():
            self.parent_view.game_active = False
            await interaction.response.edit_message(content="It's a draw!", view=self.parent_view)
        else:
            self.parent_view.turn = 1 - self.parent_view.turn
            await interaction.response.edit_message(
                content=f"{self.parent_view.players[self.parent_view.turn].mention}'s turn",
                view=self.parent_view
            )

class STicTacToeView(View):
    def __init__(self, player1, player2):
        super().__init__(timeout=None)
        self.players = [player1, player2]
        self.turn = 0
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_active = True

        for i in range(3):
            for j in range(3):
                self.add_item(STicTacToeButton(i, j, self))

    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != "":
                return True
            if b[0][i] == b[1][i] == b[2][i] != "":
                return True
        if b[0][0] == b[1][1] == b[2][2] != "":
            return True
        if b[0][2] == b[1][1] == b[2][0] != "":
            return True
        return False

    def is_draw(self):
        return all(cell != "" for row in self.board for cell in row)
