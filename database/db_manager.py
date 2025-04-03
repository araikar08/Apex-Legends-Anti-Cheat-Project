import sqlite3
import os
from config import DB_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DB_PATH
        self._ensure_db_directory()
        self.conn = None
        self.cursor = None

    def _ensure_db_directory(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def initialize_database(self):
        self.connect()
        with open('database/schema.sql', 'r') as f:
            self.cursor.executescript(f.read())
        self.conn.commit()
        self.close()

    def add_player(self, uid, username, platform, level):
        self.connect()
        self.cursor.execute('''
            INSERT OR REPLACE INTO players (uid, username, platform, level)
            VALUES (?, ?, ?, ?)
        ''', (uid, username, platform, level))
        self.conn.commit()
        self.close()

    def add_player_stats(self, player_uid, kills, deaths, headshots, damage, matches_played):
        self.connect()
        self.cursor.execute('''
            INSERT INTO player_stats 
            (player_uid, kills, deaths, headshots, damage, matches_played)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_uid, kills, deaths, headshots, damage, matches_played))
        self.conn.commit()
        self.close()

    def add_suspicious_player(self, player_uid, reason, confidence_score):
        self.connect()
        self.cursor.execute('''
            INSERT INTO suspicious_players (player_uid, reason, confidence_score)
            VALUES (?, ?, ?)
        ''', (player_uid, reason, confidence_score))
        self.conn.commit()
        self.close()

    def get_player_stats(self, player_uid):
        self.connect()
        self.cursor.execute('''
            SELECT * FROM player_stats 
            WHERE player_uid = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (player_uid,))
        result = self.cursor.fetchone()
        self.close()
        return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help='Initialize database')
    args = parser.parse_args()

    if args.init:
        db = DatabaseManager()
        db.initialize_database()
        print("Database initialized successfully") 