from database.db_manager import DatabaseManager
from config import (
    SUSPICIOUS_KDR_THRESHOLD,
    SUSPICIOUS_HEADSHOT_RATIO,
    MIN_MATCHES_FOR_ANALYSIS
)

class PlayerAnalyzer:
    def __init__(self):
        self.db = DatabaseManager()

    # Basic stat calculations
    def calculate_kdr(self, kills, deaths):
        return kills / deaths if deaths > 0 else kills

    def calculate_headshot_ratio(self, headshots, kills):
        return headshots / kills if kills > 0 else 0

    # Main analysis function
    def analyze_player(self, player_uid):
        stats = self.db.get_player_stats(player_uid)
        if not stats:
            return None

        _, _, kills, deaths, headshots, damage, matches_played, _ = stats

        if matches_played < MIN_MATCHES_FOR_ANALYSIS:
            return None

        kdr = self.calculate_kdr(kills, deaths)
        hs_ratio = self.calculate_headshot_ratio(headshots, kills)
        dpm = damage / matches_played

        # Check for suspicious activity
        suspicious = False
        reasons = []
        confidence = 0.0

        if kdr > SUSPICIOUS_KDR_THRESHOLD:
            suspicious = True
            reasons.append(f"High KDR: {kdr:.2f}")
            confidence += 0.4

        if hs_ratio > SUSPICIOUS_HEADSHOT_RATIO:
            suspicious = True
            reasons.append(f"High headshot ratio: {hs_ratio:.2%}")
            confidence += 0.3

        if dpm > 2000:  # High damage threshold
            suspicious = True
            reasons.append(f"High damage per match: {dpm:.0f}")
            confidence += 0.3

        if suspicious:
            self.db.add_suspicious_player(
                player_uid,
                ' | '.join(reasons),
                min(confidence, 1.0)
            )

        return {
            'kdr': kdr,
            'headshot_ratio': hs_ratio,
            'damage_per_match': dpm,
            'suspicious': suspicious,
            'reasons': reasons,
            'confidence': confidence
        } 