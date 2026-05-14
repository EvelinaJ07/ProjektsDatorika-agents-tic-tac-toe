# Tic Tac Toe AI Game - Complete Project Structure

## 📁 Project Files Overview

All files have been generated and organized in the `agents-tic-tac-toe` branch. Below is the complete file structure:

```
tic-tac-toe-ai-game/
├── backend/
│   ├── app.py              (Flask REST API server - 180+ lines)
│   ├── game_logic.py       (Board & win detection - 100+ lines)
│   ├── ai.py              (AI with Minimax algorithm - 150+ lines)
│   ├── database.py        (SQLite operations - 120+ lines)
│   └── requirements.txt    (Python dependencies)
│
├── frontend/
│   ├── index.html         (Game UI structure - 90+ lines)
│   ├── style.css          (Light blue theme styling - 180+ lines)
│   └── script.js          (Game logic & API calls - 250+ lines)
│
├── requirements.txt        (Flask, Flask-CORS)
├── README.md              (Comprehensive documentation)
├── .gitignore            (Python, SQLite, IDE files)
└── setup.py              (Auto-setup script)
└── setup.bat             (Windows batch setup script)
```

## 🚀 Quick Start (3 Steps)

### Step 1: Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Flask Backend Server
```bash
python backend/app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 3: Open the Frontend
Open this URL in your browser:
```
file:///full/path/to/frontend/index.html
```

Or use Python's HTTP server:
```bash
cd frontend
python -m http.server 8000
```
Then visit: `http://localhost:8000`

---

## 📋 What Each File Does

### Backend Files

#### `backend/app.py`
- **Purpose**: Flask web server & REST API
- **Endpoints**:
  - `POST /api/make-move` - Process player move, get AI move
  - `POST /api/save-result` - Save game to database
  - `GET /api/leaderboard` - Fetch top players
  - `GET /health` - Health check

#### `backend/game_logic.py`
- **Purpose**: Game board representation & rules
- **Class**: `Board`
  - `make_move(position, player)` - Place symbol
  - `is_winner(player)` - Check for win
  - `is_draw()` - Check for draw
  - `get_available_moves()` - Get valid positions
  - `get_board_state()` - Return board copy

#### `backend/ai.py`
- **Purpose**: AI opponent with 3 difficulty levels
- **Class**: `AIPlayer`
  - `_easy_move()` - Random moves
  - `_medium_move()` - Blocks & strategic
  - `_hard_move()` - Minimax algorithm
  - `_minimax()` - Minimax with alpha-beta pruning

#### `backend/database.py`
- **Purpose**: SQLite database operations
- **Functions**:
  - `init_database()` - Create tables
  - `save_game_result()` - Store game
  - `get_leaderboard()` - Fetch top players
  - `get_player_stats()` - Player statistics

### Frontend Files

#### `frontend/index.html`
- **Purpose**: Game UI structure
- **Screens**:
  - Menu (nickname, difficulty selection)
  - Game board (3x3 grid)
  - Leaderboard (player stats)

#### `frontend/style.css`
- **Purpose**: Light blue theme styling
- **Colors**:
  - Primary: `#1976d2` (Blue)
  - Light: `#e3f2fd` (Light Blue)
  - Red: `#f44336` (AI symbol)
  - Background: Gradient purple

#### `frontend/script.js`
- **Purpose**: Game logic & API communication
- **Functions**:
  - `startGame()` - Initialize game
  - `handleCellClick()` - Process player move
  - `saveGameResult()` - Save to database
  - `loadLeaderboard()` - Fetch rankings

---

## 🎮 How to Play

1. **Enter Nickname**: Type your name
2. **Select Difficulty**: Easy, Medium, or Hard
3. **Click Start Game**
4. **Make Moves**: Click empty cells to place X
5. **View Results**: After game ends, see result and leaderboard
6. **Check Leaderboard**: See top players by wins

---

## 🤖 AI Difficulty Levels Explained

### Easy (Random)
- Makes completely random moves
- No strategy whatsoever
- Very easy to beat

### Medium (Strategic)
- Tries to win (3 in a row)
- Blocks your winning moves
- Prefers center, then corners
- Balanced challenge

### Hard (Minimax)
- Uses Minimax algorithm with alpha-beta pruning
- Plays optimally
- Very difficult to beat
- Can force a draw with perfect play

---

## 📊 Database Structure

### Table: `games`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| player_name | TEXT | Player's nickname |
| difficulty | TEXT | Easy/Medium/Hard |
| result | TEXT | Win/Loss/Draw |
| created_at | DATETIME | Timestamp |

**Database File**: `game.db` (auto-created on first run)

---

## 🔌 API Endpoint Examples

### Make Move
```bash
curl -X POST http://127.0.0.1:5000/api/make-move \
  -H "Content-Type: application/json" \
  -d '{
    "board": [null, "X", null, ...],
    "player_move": 0,
    "difficulty": "hard"
  }'
```

### Save Result
```bash
curl -X POST http://127.0.0.1:5000/api/save-result \
  -H "Content-Type: application/json" \
  -d '{
    "player_name": "Alex",
    "difficulty": "Hard",
    "result": "Win"
  }'
```

### Get Leaderboard
```bash
curl http://127.0.0.1:5000/api/leaderboard?limit=10
```

---

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Use a different port
python backend/app.py  # Change port in app.py
```

### CORS Errors
- Make sure backend runs on `http://127.0.0.1:5000`
- Frontend sends requests to the correct URL
- Flask-CORS is installed

### Game Results Not Saving
- Check `game.db` exists
- Verify backend has write permissions
- Check Flask console for errors

### Can't Open Frontend HTML
- Use Python HTTP server instead of `file://` protocol
- Or use a browser extension to serve files locally

---

## 📝 Code Quality Features

✅ **Comments throughout code** - Every function has docstrings  
✅ **Error handling** - Try/except blocks in API routes  
✅ **Input validation** - Board moves validated  
✅ **Responsive design** - Works on mobile & desktop  
✅ **XSS protection** - HTML escaping in leaderboard  
✅ **Optimized AI** - Alpha-beta pruning in Minimax  

---

## 🎯 Learning Outcomes

This project demonstrates:
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask REST API
- **Database**: SQLite with CRUD operations
- **API**: RESTful endpoint design
- **Game Logic**: Board representation, win detection
- **AI**: Minimax algorithm with optimization
- **Full Stack**: Complete web application flow

---

## 📦 Dependencies

### Python
- Flask 2.3.3 - Web framework
- Flask-CORS 4.0.0 - Cross-origin requests

### Frontend
- No external dependencies - Vanilla JavaScript only
- Pure CSS - No frameworks

### Database
- SQLite 3 - Built-in, no installation needed

---

## 🔮 Future Enhancements

Possible additions:
- Multiplayer mode (PvP)
- User authentication
- Win streak tracking
- Sound effects & animations
- Elo rating system
- Online leaderboard
- Mobile app version

---

## 📄 License

Created for educational purposes as a programming class assignment.

---

**Project Status**: ✅ Complete & Ready to Run

All files are organized, documented, and ready for local development.
