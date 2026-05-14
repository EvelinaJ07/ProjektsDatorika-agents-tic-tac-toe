"""
Flask Backend for Tic Tac Toe AI Game
Provides REST API endpoints for the frontend to interact with game logic and database.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from game_logic import Board
from ai import AIPlayer
from database import init_database, save_game_result, get_leaderboard

app = Flask(__name__)
CORS(app)

# Initialize database on startup
init_database()


@app.route('/api/make-move', methods=['POST'])
def make_move():
    """
    Handle player move and return AI move.
    Expected request body:
    {
        "board": [list of 9 elements representing board state],
        "player_move": position (0-8),
        "difficulty": "easy", "medium", or "hard"
    }
    Returns:
    {
        "board": updated board state,
        "ai_move": AI move position,
        "player_wins": boolean,
        "ai_wins": boolean,
        "is_draw": boolean,
        "game_over": boolean
    }
    """
    try:
        data = request.get_json()

        # Validate input
        if not data or 'board' not in data or 'player_move' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        # Recreate board from frontend state
        board = Board()
        board.grid = data['board']

        player_move = data['player_move']
        difficulty = data.get('difficulty', 'medium')

        # Make player move
        if not board.make_move(player_move, 'X'):
            return jsonify({'error': 'Invalid move'}), 400

        # Check if player won
        player_wins = board.is_winner('X')
        if player_wins:
            return jsonify({
                'board': board.get_board_state(),
                'ai_move': None,
                'player_wins': True,
                'ai_wins': False,
                'is_draw': False,
                'game_over': True
            })

        # Check for draw after player move
        if board.is_draw():
            return jsonify({
                'board': board.get_board_state(),
                'ai_move': None,
                'player_wins': False,
                'ai_wins': False,
                'is_draw': True,
                'game_over': True
            })

        # Get AI move
        ai = AIPlayer(difficulty)
        ai_move = ai.get_move(board)

        if ai_move is None:
            return jsonify({'error': 'No valid AI move'}), 400

        board.make_move(ai_move, 'O')

        # Check if AI won
        ai_wins = board.is_winner('O')
        if ai_wins:
            return jsonify({
                'board': board.get_board_state(),
                'ai_move': ai_move,
                'player_wins': False,
                'ai_wins': True,
                'is_draw': False,
                'game_over': True
            })

        # Check for draw after AI move
        is_draw = board.is_draw()

        return jsonify({
            'board': board.get_board_state(),
            'ai_move': ai_move,
            'player_wins': False,
            'ai_wins': False,
            'is_draw': is_draw,
            'game_over': is_draw
        })

    except Exception as e:
        print(f"Error in make_move: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/save-result', methods=['POST'])
def save_result():
    """
    Save game result to database.
    Expected request body:
    {
        "player_name": "nickname",
        "difficulty": "Easy", "Medium", or "Hard",
        "result": "Win", "Loss", or "Draw"
    }
    Returns:
    {
        "success": boolean,
        "message": string
    }
    """
    try:
        data = request.get_json()

        # Validate input
        required_fields = ['player_name', 'difficulty', 'result']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        success = save_game_result(
            data['player_name'],
            data['difficulty'],
            data['result']
        )

        if success:
            return jsonify({'success': True, 'message': 'Game result saved'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save result'}), 500

    except Exception as e:
        print(f"Error in save_result: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    """
    Get leaderboard data.
    Query parameters:
        limit: Maximum number of players (default: 10)
    Returns:
    {
        "leaderboard": [
            {
                "player_name": "name",
                "wins": number,
                "losses": number,
                "draws": number,
                "total_games": number
            },
            ...
        ]
    }
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        leaderboard_data = get_leaderboard(limit)

        return jsonify({'leaderboard': leaderboard_data})

    except Exception as e:
        print(f"Error in leaderboard: {e}")
        return jsonify({'leaderboard': []}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Run Flask app in debug mode for development
    app.run(debug=True, host='127.0.0.1', port=5000)
