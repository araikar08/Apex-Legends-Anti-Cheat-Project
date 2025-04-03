import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class MLAnomalyDetector:
    def __init__(self):
        # Expect 10% of players to be suspicious
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        
    # Prep stats for ML model
    def prepare_features(self, player_stats):
        features = np.array([
            player_stats['kdr'],
            player_stats['headshot_ratio'],
            player_stats['damage_per_match']
        ]).reshape(1, -1)
        return self.scaler.fit_transform(features)
    
    # Check if player stats look fishy
    def detect_anomalies(self, player_stats):
        try:
            features = self.prepare_features(player_stats)
            anomaly_score = self.model.fit_predict(features)[0]
            ml_confidence = (1 - anomaly_score) / 2
            
            return {
                'is_anomaly': anomaly_score == -1,
                'ml_confidence': ml_confidence,
                'features': features[0].tolist()
            }
        except Exception as e:
            print(f"ML analysis error: {str(e)}")
            return {
                'is_anomaly': False,
                'ml_confidence': 0.0,
                'features': []
            } 