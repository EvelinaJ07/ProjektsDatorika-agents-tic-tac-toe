"""
Database Module
Handles SQLite operations for storing and retrieving game results.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = 'game.db'


def init_database():
    """Initialize the database with the games table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def save_game_result(player_name, difficulty, result):
    """
    Save a game result to the database.
    Args:
        player_name: Player's nickname
        difficulty: Difficulty level ('Easy', 'Medium', 'Hard')
        result: Game result ('Win', 'Loss', 'Draw')
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO games (player_name, difficulty, result, created_at)
            VALUES (?, ?, ?, ?)
        ''', (player_name, difficulty, result, datetime.now().isoformat()))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving game result: {e}")
        return False


def get_leaderboard(limit=10):
    """
    Get the leaderboard data sorted by wins.
    Args:
        limit: Maximum number of players to return
    Returns:
        List of dictionaries with player_name, wins, losses, draws
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                player_name,
                SUM(CASE WHEN result = 'Win' THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN result = 'Loss' THEN 1 ELSE 0 END) as losses,
                SUM(CASE WHEN result = 'Draw' THEN 1 ELSE 0 END) as draws
            FROM games
            GROUP BY player_name
            ORDER BY wins DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        leaderboard = [
            {
                'player_name': row[0],
                'wins': row[1],
                'losses': row[2],
                'draws': row[3],
                'total_games': row[1] + row[2] + row[3]
            }
            for row in rows
        ]

        return leaderboard
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []


def get_player_stats(player_name):
    """
    Get statistics for a specific player.
    Args:
        player_name: Player's nickname
    Returns:
        Dictionary with player stats or None if not found
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                player_name,
                SUM(CASE WHEN result = 'Win' THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN result = 'Loss' THEN 1 ELSE 0 END) as losses,
                SUM(CASE WHEN result = 'Draw' THEN 1 ELSE 0 END) as draws
            FROM games
            WHERE player_name = ?
            GROUP BY player_name
        ''', (player_name,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'player_name': row[0],
                'wins': row[1],
                'losses': row[2],
                'draws': row[3],
                'total_games': row[1] + row[2] + row[3]
            }
        return None
    except Exception as e:
        print(f"Error fetching player stats: {e}")
        return None
