-- Players table
CREATE TABLE IF NOT EXISTS players (
    uid TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    platform TEXT NOT NULL,
    level INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Player stats table
CREATE TABLE IF NOT EXISTS player_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_uid TEXT,
    kills INTEGER,
    deaths INTEGER,
    headshots INTEGER,
    damage INTEGER,
    matches_played INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_uid) REFERENCES players(uid)
);

-- Suspicious players table
CREATE TABLE IF NOT EXISTS suspicious_players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_uid TEXT,
    reason TEXT,
    confidence_score REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_uid) REFERENCES players(uid)
); 