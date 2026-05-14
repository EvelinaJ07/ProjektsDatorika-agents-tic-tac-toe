"""
Flask Backend for Tic Tac Toe AI Game
Provides REST API endpoints for the frontend to interact with game logic and database.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from game_logic import Board
from ai import AIPlayer
from database import init_database, save_game_result, get_leaderboard

app = Flask(__name__)
CORS(app)

# Initialize database on startup
init_database()


# =========================
# 🌐 FRONTEND ROUTES (NEW)
# =========================

@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('frontend', path)


# =========================
# 🎮 GAME API
# =========================

@app.route('/api/make-move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()

        if not data or 'board' not in data or 'player_move' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        board = Board()
        board.grid = data['board']

        player_move = data['player_move']
        difficulty = data.get('difficulty', 'medium')

        if not board.make_move(player_move, 'X'):
            return jsonify({'error': 'Invalid move'}), 400

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

        if board.is_draw():
            return jsonify({
                'board': board.get_board_state(),
                'ai_move': None,
                'player_wins': False,
                'ai_wins': False,
                'is_draw': True,
                'game_over': True
            })

        ai = AIPlayer(difficulty)
        ai_move = ai.get_move(board)

        if ai_move is None:
            return jsonify({'error': 'No valid AI move'}), 400

        board.make_move(ai_move, 'O')

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
    try:
        data = request.get_json()

        required_fields = ['player_name', 'difficulty', 'result']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        success = save_game_result(
            data['player_name'],
            data['difficulty'],
            data['result']
        )

        if success:
            return jsonify({'success': True, 'message': 'Spēles rezultāts saglabāts!'})
        else:
            return jsonify({'success': False, 'message': 'Neizdevās saglabāt rezultātu!'}), 500

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    try:
        limit = request.args.get('limit', 10, type=int)
        leaderboard_data = get_leaderboard(limit)

        return jsonify({'leaderboard': leaderboard_data})

    except Exception as e:
        print(f"Error in leaderboard: {e}")
        return jsonify({'leaderboard': []}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


# =========================
# 🚀 RUN APP
# =========================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
