# 🎮 Tic Tac Toe AI Game - Setup Instructions

## ✨ Project Summary

A complete full-stack web application featuring:
- **Frontend**: HTML5, CSS3, Vanilla JavaScript with light blue UI theme
- **Backend**: Python Flask REST API with SQLite database
- **AI**: Three difficulty levels including Minimax algorithm
- **Database**: Game results storage and leaderboard
- **Responsive**: Works on desktop and mobile devices

---

## 📋 Prerequisites

- **Python 3.7+** (Download from python.org)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Terminal/Command Prompt** for running commands
- **Text editor** (optional, for viewing/editing files)

---

## 🚀 Installation & Running

### Option A: Automated Setup (Recommended)

#### Windows:
```bash
setup.bat
pip install -r requirements.txt
python backend/app.py
```

#### macOS/Linux:
```bash
python setup.py
pip install -r requirements.txt
python backend/app.py
```

### Option B: Manual Setup (Step by Step)

#### Step 1: Navigate to Project Directory
```bash
cd /path/to/tic-tac-toe-ai-game
```

#### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask 2.3.3 - Web framework
- Flask-CORS 4.0.0 - Handle browser requests

#### Step 3: Run the Backend Server
```bash
python backend/app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

✅ Backend is now running!

#### Step 4: Open the Frontend (Choose One)

**Option 1: Direct File (Simple)**
```
In your browser, go to:
file:///full/path/to/frontend/index.html
```

Replace `/full/path/to` with your actual path, e.g.:
- Windows: `file:///C:/Users/YourName/Documents/tic-tac-toe-ai-game/frontend/index.html`
- macOS: `file:///Users/YourName/tic-tac-toe-ai-game/frontend/index.html`
- Linux: `file:///home/username/tic-tac-toe-ai-game/frontend/index.html`

**Option 2: Python HTTP Server (Recommended)**
```bash
# In a NEW terminal/command prompt:
cd frontend
python -m http.server 8000
```

Then open in browser:
```
http://localhost:8000
```

---

## 🎮 Playing the Game

1. **Enter Your Nickname**
   - Type any name (max 20 characters)
   - Press Enter or click "Start Game"

2. **Select Difficulty**
   - **Easy**: AI makes random moves (easy to beat)
   - **Medium**: AI blocks wins and plays strategically (balanced)
   - **Hard**: AI uses Minimax algorithm (very difficult)

3. **Play the Game**
   - You are **X** (blue color)
   - AI is **O** (red color)
   - Click any empty cell to make your move
   - AI automatically responds

4. **Win Conditions**
   - **3 in a row** (horizontal, vertical, or diagonal) = You Win!
   - **AI gets 3 in a row** = AI Wins
   - **Board fills up** with no winner = Draw

5. **View Results**
   - After each game, results are saved to database
   - Click "Play Again" to replay
   - Click "View Leaderboard" to see rankings
   - Click "Back to Menu" to return to start

---

## 📊 Project Structure

```
tic-tac-toe-ai-game/
│
├── backend/
│   ├── app.py              # Flask server & API routes
│   ├── game_logic.py       # Board logic & win detection  
│   ├── ai.py              # AI with 3 difficulty levels
│   ├── database.py        # SQLite database operations
│   └── game.db            # Game results database (auto-created)
│
├── frontend/
│   ├── index.html         # Game interface HTML
│   ├── style.css          # Light blue theme styling
│   └── script.js          # Game UI & API communication
│
├── requirements.txt        # Python dependencies
├── README.md              # Detailed documentation
├── PROJECT_STRUCTURE.md   # File structure guide
├── SETUP_INSTRUCTIONS.md  # This file
├── setup.py              # Auto-setup script
├── setup.bat             # Windows setup script
└── .gitignore           # Git ignore patterns
```

---

## 🔌 API Endpoints

The backend provides these REST API endpoints:

### 1. Make Move
```
POST /api/make-move
```
Processes player move and returns AI response.

### 2. Save Result
```
POST /api/save-result
```
Saves completed game to database.

### 3. Get Leaderboard
```
GET /api/leaderboard?limit=10
```
Returns top players sorted by wins.

### 4. Health Check
```
GET /health
```
Verifies backend is running.

---

## 🤖 AI Difficulty Levels

### Easy Mode
- Makes **completely random** moves
- No intelligence whatsoever
- Perfect for beginners
- Easy to beat

### Medium Mode  
- Tries to **win** (gets 3 in a row)
- **Blocks** your winning moves
- Prefers **center** then **corners**
- Good challenge level

### Hard Mode
- Uses **Minimax algorithm**
- Plays **optimally**
- Implements **alpha-beta pruning**
- Very difficult to beat
- Expert level play

---

## 📁 Where Files Are Stored

### Database (`game.db`)
- Location: Project root directory
- Created automatically on first game
- Stores: Player names, difficulty, results, timestamps
- Format: SQLite3

### Browser Cache
- Stored locally in your browser
- No personal data collected
- Can clear without affecting game

---

## 🐛 Troubleshooting

### Problem: "Port 5000 is already in use"
**Solution**: Another application is using port 5000
```bash
# Use a different port (edit app.py line at bottom):
# Change: app.run(port=5000)
# To: app.run(port=5001)
python backend/app.py
```

### Problem: "Cannot fetch from http://127.0.0.1:5000"
**Solution**: Backend is not running
```bash
# Make sure backend is running in another terminal:
python backend/app.py
# You should see "Running on http://127.0.0.1:5000"
```

### Problem: "Browser blocks requests (CORS error)"
**Solution**: Flask-CORS not installed or frontend using wrong URL
```bash
pip install -r requirements.txt  # Reinstall
# Make sure frontend requests go to: http://127.0.0.1:5000/api
```

### Problem: "Game results not saving"
**Solution**: Database file permissions issue
```bash
# Check if game.db exists in project root
# Ensure folder has write permissions
# Try deleting game.db and restarting (will be recreated)
```

### Problem: "Cannot open frontend/index.html"
**Solution**: Browser security blocks local file protocol
```bash
# Use Python HTTP server instead:
cd frontend
python -m http.server 8000
# Then visit: http://localhost:8000
```

---

## ⚙️ Configuration

### Change Backend Port
Edit `backend/app.py` (last lines):
```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)  # Change port here
```

### Change API URL in Frontend
Edit `frontend/script.js` (line 12):
```javascript
const API_URL = 'http://127.0.0.1:5000/api';  // Change if needed
```

### Customize UI Theme
Edit `frontend/style.css` colors:
```css
#1976d2  /* Primary blue */
#e3f2fd  /* Light blue */
#f44336  /* Red for AI */
```

---

## 💡 Tips for Best Experience

1. **Use Python HTTP Server** for frontend instead of file:// protocol
2. **Keep both terminal windows open** (backend + optional frontend server)
3. **Hard difficulty** takes a moment - AI is thinking (that's normal!)
4. **Results are auto-saved** after each game - no manual save needed
5. **Clear browser cache** if experiencing issues

---

## 📱 Browser Compatibility

✅ Chrome/Chromium - Full support  
✅ Firefox - Full support  
✅ Safari - Full support  
✅ Edge - Full support  
✅ Mobile browsers - Responsive design  

---

## 🔒 Security Notes

- No user authentication (educational project)
- Database stores only game results (player name, difficulty, result)
- CORS enabled for development
- Input sanitization on leaderboard display
- No sensitive data collected

---

## 📚 Project Files Explained

### Backend Files

**app.py** (180+ lines)
- Flask application setup
- REST API routes
- Request/response handling
- CORS configuration

**game_logic.py** (100+ lines)
- Board class with game rules
- Move validation
- Win condition checking
- Draw detection

**ai.py** (150+ lines)
- AIPlayer class
- Easy, Medium, Hard difficulty strategies
- Minimax algorithm implementation
- Alpha-beta pruning optimization

**database.py** (120+ lines)
- SQLite database initialization
- Game result storage
- Leaderboard queries
- Player statistics

### Frontend Files

**index.html** (90+ lines)
- Menu screen (nickname, difficulty selection)
- Game board (3x3 grid)
- Leaderboard table
- Semantic HTML structure

**style.css** (180+ lines)
- Light blue color theme
- Responsive grid layout
- Hover effects and animations
- Mobile-friendly design
- Custom scrollbar styling

**script.js** (250+ lines)
- Game state management
- Event handling
- API communication
- Board rendering
- Leaderboard loading
- XSS protection

---

## 🎓 Learning Objectives

This project teaches:
- ✅ Full-stack web development
- ✅ REST API design and implementation
- ✅ Database design and operations
- ✅ Game logic and AI algorithms
- ✅ Frontend/backend communication
- ✅ HTML5, CSS3, JavaScript
- ✅ Python backend development
- ✅ Responsive web design

---

## 📞 Support

If you encounter issues:

1. **Check Prerequisites** - Python 3.7+, Modern browser
2. **Review Troubleshooting** section above
3. **Check Terminal Output** - Look for error messages
4. **Browser Console** - Press F12, check "Console" tab
5. **Flask Console** - Look at terminal running backend

---

## ✨ Enjoy the Game!

You're all set to play Tic Tac Toe against AI! 🎉

Try beating the Hard difficulty for a real challenge!

---

**Last Updated**: May 14, 2026  
**Status**: ✅ Complete and Production Ready
