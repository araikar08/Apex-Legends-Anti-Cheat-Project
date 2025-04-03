from apex_client import ApexClient
from database.db_manager import DatabaseManager
from config import PLATFORMS

class DataFetcher:
    def __init__(self):
        self.client = ApexClient()
        self.db = DatabaseManager()

    def fetch_and_store_player_data(self, player_name, platform):
        if platform not in PLATFORMS.values():
            raise ValueError(f"Invalid platform. Must be one of {list(PLATFORMS.values())}")

        # Get player data
        data = self.client.get_player_stats(player_name, platform)
        
        if 'Error' in data:
            raise Exception(f"Error fetching player data: {data['Error']}")

        # Extract relevant stats
        stats = data.get('global', {})
        uid = data.get('global', {}).get('uid')
        level = stats.get('level', 0)
        
        # Store in database
        self.db.add_player(uid, player_name, platform, level)
        
        # Store detailed stats
        self.db.add_player_stats(
            uid,
            stats.get('kills', 0),
            stats.get('deaths', 0),
            stats.get('headshots', 0),
            stats.get('damage', 0),
            stats.get('matches_played', 0)
        )

        return {
            'uid': uid,
            'stats': stats
        }

    def fetch_multiple_players(self, player_list):
        results = []
        for player in player_list:
            try:
                result = self.fetch_and_store_player_data(
                    player['name'],
                    player['platform']
                )
                results.append(result)
            except Exception as e:
                print(f"Error processing {player['name']}: {str(e)}")
        return results 