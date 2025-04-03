# Apex Anti-Cheat Analysis System

A Python-based system for detecting suspicious player behavior in Apex Legends. Uses statistical analysis and machine learning to identify potential cheaters.

## Architecture

```
apex_anti/
├── api/                    # API interaction layer
│   ├── apex_client.py     # Handles API requests
│   └── data_fetcher.py    # Fetches and processes player data
├── analysis/              # Analysis modules
│   ├── player_analyzer.py # Basic stat analysis
│   ├── ml_analyzer.py     # ML-based anomaly detection
│   └── anomaly_detector.py# Pattern recognition
├── database/              # Data persistence
│   ├── db_manager.py      # Database operations
│   └── models.py          # Data models
├── docs/                  # Documentation
│   └── player_comparison_example.md
└── main.py               # Entry point
```

## Features

- Real-time player stat analysis
- Machine learning-based anomaly detection
- Pattern recognition for suspicious behavior
- Historical data tracking
- Confidence scoring system

## Setup

1. Clone the repo
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your API key in `config.py`:
   ```python
   API_KEY = "your_key_here"
   ```

## Usage

Analyze a player:
```bash
python main.py --player "PlayerName" --platform PC
```

## How It Works

The system uses multiple detection methods:

1. **Statistical Analysis**
   - KDR thresholds
   - Headshot ratio analysis
   - Damage per match calculations

2. **Machine Learning**
   - Isolation Forest for anomaly detection
   - Feature normalization
   - Confidence scoring

3. **Pattern Recognition**
   - Rank progression analysis
   - Performance consistency checks
   - Historical data comparison

## Security Note

Never commit your API key. The `.gitignore` file is configured to prevent accidental commits of sensitive data.

## Example Analysis

See `docs/player_comparison_example.md` for a detailed comparison between legitimate and suspicious players.

## Contributing

Feel free to submit issues and pull requests. Make sure to follow the existing code style and add tests for new features. 