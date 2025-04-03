# Apex Legends Player Behavior Analysis System

A system for analyzing player behavior in Apex Legends to detect potential cheating patterns using statistical analysis and anomaly detection.

## Features

- Real-time player statistics tracking
- Statistical analysis of player performance
- Anomaly detection for suspicious behavior
- SQL database for storing and querying player data
- Automated reporting system

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/apex_anti.git
cd apex_anti
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
- Get an API key from https://apexlegendsapi.com/
- Create a `.env` file in the root directory
- Add your API key: `APEX_API_KEY=your_key_here`

4. Initialize the database:
```bash
python -m database.db_manager --init
```

## Usage

Run the main analysis script:
```bash
python main.py
```

## Project Structure

- `api/`: API client and data fetching modules
- `analysis/`: Core analysis and detection logic
- `database/`: Database management and schema
- `utils/`: Helper functions and logging
- `config.py`: Configuration settings
- `main.py`: Main entry point

## Contributing

Feel free to submit issues and enhancement requests.

## License

MIT License 