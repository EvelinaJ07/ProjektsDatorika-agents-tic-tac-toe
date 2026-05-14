"""
AI Module
Implements three difficulty levels for the AI opponent:
- Easy: Random moves
- Medium: Blocks obvious wins, makes strategic moves
- Hard: Minimax algorithm with alpha-beta pruning
"""

import random


class AIPlayer:
    """AI opponent for Tic Tac Toe."""

    def __init__(self, difficulty='medium'):
        """
        Initialize AI player.
        Args:
            difficulty: 'easy', 'medium', or 'hard'
        """
        self.difficulty = difficulty.lower()
        self.ai_symbol = 'O'
        self.player_symbol = 'X'

    def get_move(self, board):
        """
        Get the AI's next move based on difficulty level.
        Args:
            board: Board object representing current game state
        Returns:
            Position (0-8) where AI should move
        """
        if self.difficulty == 'easy':
            return self._easy_move(board)
        elif self.difficulty == 'medium':
            return self._medium_move(board)
        elif self.difficulty == 'hard':
            return self._hard_move(board)
        else:
            return self._easy_move(board)

    def _easy_move(self, board):
        """Easy difficulty: Random move from available positions."""
        available = board.get_available_moves()
        return random.choice(available) if available else None

    def _medium_move(self, board):
        """Medium difficulty: Block wins, win if possible, else strategic."""
        available = board.get_available_moves()

        # Try to win
        for move in available:
            board.make_move(move, self.ai_symbol)
            if board.is_winner(self.ai_symbol):
                board.undo_move(move)
                return move
            board.undo_move(move)

        # Block player from winning
        for move in available:
            board.make_move(move, self.player_symbol)
            if board.is_winner(self.player_symbol):
                board.undo_move(move)
                return move
            board.undo_move(move)

        # Take center if available
        if 4 in available:
            return 4

        # Take corners
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if c in available]
        if available_corners:
            return random.choice(available_corners)

        # Take any available
        return random.choice(available) if available else None

    def _hard_move(self, board):
        """Hard difficulty: Minimax algorithm with alpha-beta pruning."""
        best_score = float('-inf')
        best_move = None
        available = board.get_available_moves()

        for move in available:
            board.make_move(move, self.ai_symbol)
            score = self._minimax(board, 0, False, float('-inf'), float('inf'))
            board.undo_move(move)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move if best_move is not None else random.choice(available)

    def _minimax(self, board, depth, is_maximizing, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.
        Args:
            board: Board object
            depth: Current search depth
            is_maximizing: True if AI's turn, False if player's turn
            alpha: Alpha value for pruning
            beta: Beta value for pruning
        Returns:
            Score for the board position
        """
        # Terminal states
        if board.is_winner(self.ai_symbol):
            return 10 - depth
        if board.is_winner(self.player_symbol):
            return depth - 10
        if board.is_draw():
            return 0

        available = board.get_available_moves()

        if is_maximizing:
            # AI's turn: maximize score
            max_score = float('-inf')
            for move in available:
                board.make_move(move, self.ai_symbol)
                score = self._minimax(board, depth + 1, False, alpha, beta)
                board.undo_move(move)
                max_score = max(score, max_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_score
        else:
            # Player's turn: minimize score
            min_score = float('inf')
            for move in available:
                board.make_move(move, self.player_symbol)
                score = self._minimax(board, depth + 1, True, alpha, beta)
                board.undo_move(move)
                min_score = min(score, min_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_score
