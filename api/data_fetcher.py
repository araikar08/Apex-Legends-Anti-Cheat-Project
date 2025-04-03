from api.apex_client import ApexClient
from database.db_manager import DatabaseManager
from config import PLATFORMS
import json

class DataFetcher:
    def __init__(self):
        self.client = ApexClient()
        self.db = DatabaseManager()

    # Get and store player data
    def fetch_and_store_player_data(self, player_name, platform):
        if platform not in PLATFORMS.values():
            raise ValueError(f"Invalid platform. Must be one of {list(PLATFORMS.values())}")

        # Get player data
        data = self.client.get_player_stats(player_name, platform)
        print(f"Raw API response: {json.dumps(data, indent=2)}")
        
        if 'Error' in data:
            raise Exception(f"Error fetching player data: {data['Error']}")

        # Check player name match
        stats = data.get('global', {})
        returned_name = stats.get('name', '').lower()
        search_name = player_name.lower()
        
        if search_name not in returned_name and returned_name not in search_name:
            raise Exception(f"Player name mismatch. Searched for '{player_name}' but got '{stats.get('name')}'")

        uid = stats.get('uid')
        level = stats.get('level', 0)

        # Get total stats
        total_stats = data.get('total', {})
        legends_data = data.get('legends', {}).get('all', {})
        
        # Count kills and damage
        total_kills = 0
        total_damage = 0
        for legend in legends_data.values():
            legend_data = legend.get('data', [])
            for stat in legend_data:
                if stat.get('name') == 'BR Kills':
                    total_kills += stat.get('value', 0)
                elif stat.get('name') == 'Damage Done':
                    total_damage += stat.get('value', 0)
        
        # Use API total if available
        kills = total_stats.get('kills', {}).get('value', total_kills)
        
        # Get KD and deaths
        kd_ratio = total_stats.get('kd', {}).get('value', '-1')
        deaths = int(kills / float(kd_ratio)) if kd_ratio != '-1' and float(kd_ratio) > 0 else kills // 2
        
        # Get match count
        rank_data = stats.get('rank', {})
        matches_played = rank_data.get('rankScore', 0) // 100
        
        # Store in DB
        self.db.add_player(uid, player_name, platform, level)
        self.db.add_player_stats(
            uid,
            kills,
            deaths,
            total_stats.get('headshots', {}).get('value', 0),
            total_damage or kills * 200,
            matches_played or level * 3
        )

        return {
            'uid': uid,
            'stats': stats,
            'total_stats': {
                'kills': kills,
                'deaths': deaths,
                'kd_ratio': kd_ratio,
                'matches_played': matches_played,
                'level': level,
                'damage': total_damage
            }
        }

    # Process multiple players
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