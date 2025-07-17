# bot.py
import discord
from discord.ui import Button, View

class ATicTacToeButton(Button):
    def __init__(self, row, col, view):
        super().__init__(label="⬜", row=row)
        self.row = row
        self.col = col
        self.view_ref = view

    async def callback(self, interaction: discord.Interaction):
        view = self.view_ref
        if not view.game_active:
            await interaction.response.send_message("Game over.", ephemeral=True)
            return

        if interaction.user != view.human:
            await interaction.response.send_message("You're not the player.", ephemeral=True)
            return

        if view.board[self.row][self.col] != "":
            await interaction.response.send_message("Invalid move.", ephemeral=True)
            return

        self.label = "❌"
        self.disabled = True
        self.style = discord.ButtonStyle.danger
        view.board[self.row][self.col] = "X"

        if view.check_winner("X"):
            view.game_active = False
            await interaction.response.edit_message(content="You win! 🎉", view=view)
            return
        if view.is_draw():
            view.game_active = False
            await interaction.response.edit_message(content="It's a draw!", view=view)
            return

        # AI Move
        ai_row, ai_col = view.best_move()
        view.board[ai_row][ai_col] = "O"
        for item in view.children:
            if isinstance(item, ATicTacToeButton) and item.row == ai_row and item.col == ai_col:
                item.label = "⭕"
                item.disabled = True
                item.style = discord.ButtonStyle.primary

        if view.check_winner("O"):
            view.game_active = False
            await interaction.response.edit_message(content="AI wins. 🤖", view=view)
            return
        if view.is_draw():
            view.game_active = False
            await interaction.response.edit_message(content="It's a draw!", view=view)
            return

        await interaction.response.edit_message(content="Your turn.", view=view)

class ATicTacToeAIView(View):
    def __init__(self, human):
        super().__init__(timeout=None)
        self.human = human
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_active = True

        for i in range(3):
            for j in range(3):
                self.add_item(ATicTacToeButton(i, j, self))

    def check_winner(self, mark):
        b = self.board
        for i in range(3):
            if all(b[i][j] == mark for j in range(3)): return True
            if all(b[j][i] == mark for j in range(3)): return True
        if all(b[i][i] == mark for i in range(3)): return True
        if all(b[i][2-i] == mark for i in range(3)): return True
        return False

    def is_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def best_move(self):
        best_score = -float("inf")
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def minimax(self, is_maximizing):
        if self.check_winner("O"):
            return 1
        elif self.check_winner("X"):
            return -1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(False)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(True)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score
