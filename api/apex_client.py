import requests
import time
from config import API_KEY, API_BASE_URL, RATE_LIMIT

class ApexClient:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = API_BASE_URL
        self.last_request_time = 0

    # Don't spam the API
    def _rate_limit(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < 1/RATE_LIMIT:
            time.sleep(1/RATE_LIMIT - time_since_last)
        self.last_request_time = time.time()

    # Make API request
    def _make_request(self, endpoint, params=None):
        self._rate_limit()
        headers = {'Authorization': self.api_key}
        url = f"{self.base_url}{endpoint}"
        print(f"\nMaking request to: {url}")
        print(f"With params: {params}")
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, dict) and 'Error' in data:
                raise Exception(f"API Error: {data['Error']}")
            
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except ValueError as e:
            raise Exception(f"Failed to parse response: {str(e)}")

    # Get player stats
    def get_player_stats(self, player_name, platform):
        print(f"\nFetching stats for player: {player_name} on platform: {platform}")
        params = {
            'player': player_name,
            'platform': platform,
            'merge': 'true'
        }
        return self._make_request('bridge', params)

    # Get player by UID
    def get_player_by_uid(self, uid, platform):
        params = {
            'uid': uid,
            'platform': platform
        }
        return self._make_request('bridge', params)

    # Get map rotation
    def get_map_rotation(self):
        return self._make_request('maprotation')

    # Check server status
    def get_server_status(self):
        return self._make_request('servers') 