import requests
import time
from config import API_KEY, API_BASE_URL, RATE_LIMIT

class ApexClient:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = API_BASE_URL
        self.last_request_time = 0

    def _rate_limit(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < 1/RATE_LIMIT:
            time.sleep(1/RATE_LIMIT - time_since_last)
        self.last_request_time = time.time()

    def _make_request(self, endpoint, params=None):
        self._rate_limit()
        headers = {'Authorization': self.api_key}
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_player_stats(self, player_name, platform):
        params = {
            'player': player_name,
            'platform': platform
        }
        return self._make_request('bridge', params)

    def get_player_by_uid(self, uid, platform):
        params = {
            'uid': uid,
            'platform': platform
        }
        return self._make_request('bridge', params)

    def get_map_rotation(self):
        return self._make_request('maprotation')

    def get_server_status(self):
        return self._make_request('servers') 