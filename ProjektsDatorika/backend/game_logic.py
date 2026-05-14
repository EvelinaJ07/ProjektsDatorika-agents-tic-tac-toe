"""
Game Logic Module
Handles board representation, move validation, and win/draw detection.
Board is represented as a 1D array with indices 0-8:
  0 1 2
  3 4 5
  6 7 8
"""


class Board:
    """Represents the Tic Tac Toe game board."""

    def __init__(self):
        """Initialize empty board: None = empty, 'X' = player, 'O' = AI."""
        self.grid = [None] * 9

    def is_valid_move(self, position):
        """Check if a move at the given position is valid."""
        return 0 <= position < 9 and self.grid[position] is None

    def make_move(self, position, player):
        """Place a player's symbol on the board."""
        if self.is_valid_move(position):
            self.grid[position] = player
            return True
        return False

    def undo_move(self, position):
        """Remove a player's symbol from the board (used by AI for analysis)."""
        if 0 <= position < 9:
            self.grid[position] = None

    def get_available_moves(self):
        """Return list of available move positions."""
        return [i for i in range(9) if self.grid[i] is None]

    def is_winner(self, player):
        """Check if the given player has won."""
        # All possible winning combinations
        winning_combos = [
            [0, 1, 2],  # Top row
            [3, 4, 5],  # Middle row
            [6, 7, 8],  # Bottom row
            [0, 3, 6],  # Left column
            [1, 4, 7],  # Middle column
            [2, 5, 8],  # Right column
            [0, 4, 8],  # Diagonal (top-left to bottom-right)
            [2, 4, 6],  # Diagonal (top-right to bottom-left)
        ]

        for combo in winning_combos:
            if all(self.grid[pos] == player for pos in combo):
                return True
        return False

    def is_draw(self):
        """Check if the game is a draw (board full and no winner)."""
        if len(self.get_available_moves()) > 0:
            return False
        return not self.is_winner('X') and not self.is_winner('O')

    def is_game_over(self):
        """Check if the game is over (win or draw)."""
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()

    def get_board_state(self):
        """Return the current board state as a list."""
        return self.grid.copy()

    def reset(self):
        """Reset the board to its initial empty state."""
        self.grid = [None] * 9
