/** Tic Tac Toe AI Game - Frontend Script */

const gameState = {
    board: [null, null, null, null, null, null, null, null, null],
    playerName: '',
    difficulty: 'medium',
    gameActive: false,
    playerTurn: true,
    gameResult: null
};

const API_URL = 'http://127.0.0.1:5000/api';

const screens = {
    menu: document.getElementById('menu-screen'),
    game: document.getElementById('game-screen'),
    leaderboard: document.getElementById('leaderboard-screen')
};

const elements = {
    nicknameInput: document.getElementById('nickname-input'),
    difficultySelect: document.getElementById('difficulty-select'),
    startBtn: document.getElementById('start-btn'),
    viewLeaderboardBtn: document.getElementById('view-leaderboard-btn'),
    gameTitle: document.getElementById('game-title'),
    gameStatus: document.getElementById('game-status'),
    boardCells: document.querySelectorAll('.board-cell'),
    restartBtn: document.getElementById('restart-btn'),
    menuBtn: document.getElementById('menu-btn'),
    backFromLeaderboardBtn: document.getElementById('back-from-leaderboard-btn'),
    leaderboardBody: document.getElementById('leaderboard-body')
};

function initEventListeners() {
    elements.startBtn.addEventListener('click', startGame);
    elements.viewLeaderboardBtn.addEventListener('click', showLeaderboard);

    elements.boardCells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });
    elements.restartBtn.addEventListener('click', restartGame);
    elements.menuBtn.addEventListener('click', goToMenu);

    elements.backFromLeaderboardBtn.addEventListener('click', goToMenu);

    elements.nicknameInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            startGame();
        }
    });
}

function switchScreen(screenName) {
    Object.values(screens).forEach(screen => screen.classList.remove('active'));
    screens[screenName].classList.add('active');
}

function startGame() {
    const nickname = elements.nicknameInput.value.trim();

    if (!nickname) {
        alert('Lūdzu, ievadiet savu vārdu, lai sākt spēli!');
        return;
    }

    gameState.playerName = nickname;
    gameState.difficulty = elements.difficultySelect.value;
    gameState.board = [null, null, null, null, null, null, null, null, null];
    gameState.gameActive = true;
    gameState.playerTurn = true;
    gameState.gameResult = null;

    elements.gameTitle.textContent = `Game vs ${gameState.difficulty.charAt(0).toUpperCase() + gameState.difficulty.slice(1)} AI`;
    updateGameStatus();
    renderBoard();
    switchScreen('game');
}

function restartGame() {
    gameState.board = [null, null, null, null, null, null, null, null, null];
    gameState.gameActive = true;
    gameState.playerTurn = true;
    gameState.gameResult = null;
    updateGameStatus();
    renderBoard();
}

function goToMenu() {
    gameState.gameActive = false;
    switchScreen('menu');
}

async function handleCellClick(event) {
    if (!gameState.gameActive || !gameState.playerTurn) {
        return;
    }

    const position = parseInt(event.target.dataset.position);

    if (gameState.board[position] !== null) {
        return;
    }

    try {
        elements.boardCells.forEach(cell => cell.classList.add('disabled'));
        elements.gameStatus.textContent = 'MI domā...';

        const response = await fetch(`${API_URL}/make-move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                board: gameState.board,
                player_move: position,
                difficulty: gameState.difficulty
            })
        });

        if (!response.ok) {
            throw new Error('Neizdevās veikt gājienu!');
        }

        const data = await response.json();

        gameState.board = data.board;
        gameState.playerTurn = !data.game_over;

        if (data.game_over) {
            gameState.gameActive = false;

            if (data.player_wins) {
                gameState.gameResult = 'Win';
                elements.gameStatus.textContent = '🎉 Tu uzvarēji!';
            } else if (data.ai_wins) {
                gameState.gameResult = 'Loss';
                elements.gameStatus.textContent = '😢 MI uzvarēja!';
            } else if (data.is_draw) {
                gameState.gameResult = 'Draw';
                elements.gameStatus.textContent = "🤝 Neizšķirts!";
            }

            await saveGameResult();
        } else {
            gameState.playerTurn = true;
            updateGameStatus();
        }

        renderBoard();
    } catch (error) {
        console.error('Error:', error);
        alert('Radās kļūda. Lūdzu, mēģiniet vēlreiz.');
        gameState.playerTurn = true;
        updateGameStatus();
    } finally {
        elements.boardCells.forEach(cell => cell.classList.remove('disabled'));
    }
}

function updateGameStatus() {
    if (!gameState.gameActive) {
        return;
    }

    if (gameState.playerTurn) {
        elements.gameStatus.textContent = 'Tava kārta (X)';
    } else {
        elements.gameStatus.textContent = "MI kārta (O)";
    }
}

function renderBoard() {
    elements.boardCells.forEach((cell, index) => {
        const value = gameState.board[index];
        cell.textContent = value || '';
        cell.classList.remove('player', 'ai');

        if (value === 'X') {
            cell.classList.add('player');
        } else if (value === 'O') {
            cell.classList.add('ai');
        }

        if (value !== null || !gameState.gameActive) {
            cell.classList.add('disabled');
        } else {
            cell.classList.remove('disabled');
        }
    });
}

async function saveGameResult() {
    try {
        const response = await fetch(`${API_URL}/save-result`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                player_name: gameState.playerName,
                difficulty: gameState.difficulty.charAt(0).toUpperCase() + gameState.difficulty.slice(1),
                result: gameState.gameResult
            })
        });

        if (!response.ok) {
            console.error('Neizdevās saglabāt rezultātu!');
        }
    } catch (error) {
        console.error('Kļūda saglabājot rezultātu:', error);
    }
}

async function showLeaderboard() {
    switchScreen('leaderboard');
    loadLeaderboard();
}

async function loadLeaderboard() {
    try {
        elements.leaderboardBody.innerHTML = '<tr class="loading"><td colspan="6">Loading...</td></tr>';

        const response = await fetch(`${API_URL}/leaderboard?limit=20`);

        if (!response.ok) {
            throw new Error('Kļūda ielādējot līderu tabulu!');
        }

        const data = await response.json();
        const leaderboard = data.leaderboard;

        if (leaderboard.length === 0) {
            elements.leaderboardBody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #999;">No games played yet</td></tr>';
            return;
        }

        let html = '';
        leaderboard.forEach((player, index) => {
            html += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${escapeHtml(player.player_name)}</td>
                    <td>${player.wins}</td>
                    <td>${player.losses}</td>
                    <td>${player.draws}</td>
                    <td>${player.total_games}</td>
                </tr>
            `;
        });

        elements.leaderboardBody.innerHTML = html;
    } catch (error) {
        console.error('Kļūda ielādējot līderu tabulu:', error);
        elements.leaderboardBody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #f44336;">Error loading leaderboard</td></tr>';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function init() {
    initEventListeners();
    elements.nicknameInput.focus();
}

document.addEventListener('DOMContentLoaded', init);
