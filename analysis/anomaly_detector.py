import numpy as np
from database.db_manager import DatabaseManager

class AnomalyDetector:
    def __init__(self):
        self.db = DatabaseManager()

    def _get_stat_distribution(self, stat_name):
        self.db.connect()
        self.db.cursor.execute(f'''
            SELECT {stat_name} FROM player_stats 
            WHERE {stat_name} > 0
        ''')
        values = [row[0] for row in self.db.cursor.fetchall()]
        self.db.close()
        return np.array(values)

    def detect_anomalies(self, player_uid):
        stats = self.db.get_player_stats(player_uid)
        if not stats:
            return None

        _, _, kills, deaths, headshots, damage, matches_played, _ = stats

        # Get distributions
        kdr_dist = self._get_stat_distribution('kills') / self._get_stat_distribution('deaths')
        hs_dist = self._get_stat_distribution('headshots') / self._get_stat_distribution('kills')
        dpm_dist = self._get_stat_distribution('damage') / self._get_stat_distribution('matches_played')

        # Calculate z-scores
        kdr = kills / deaths if deaths > 0 else kills
        hs_ratio = headshots / kills if kills > 0 else 0
        dpm = damage / matches_played if matches_played > 0 else 0

        kdr_z = (kdr - np.mean(kdr_dist)) / np.std(kdr_dist)
        hs_z = (hs_ratio - np.mean(hs_dist)) / np.std(hs_dist)
        dpm_z = (dpm - np.mean(dpm_dist)) / np.std(dpm_dist)

        # Detect anomalies (z-score > 3)
        anomalies = []
        if kdr_z > 3:
            anomalies.append(f"Extreme KDR (z-score: {kdr_z:.2f})")
        if hs_z > 3:
            anomalies.append(f"Extreme headshot ratio (z-score: {hs_z:.2f})")
        if dpm_z > 3:
            anomalies.append(f"Extreme damage per match (z-score: {dpm_z:.2f})")

        return {
            'anomalies': anomalies,
            'z_scores': {
                'kdr': kdr_z,
                'headshot_ratio': hs_z,
                'damage_per_match': dpm_z
            }
        } 