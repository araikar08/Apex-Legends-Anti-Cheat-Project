from database.db_manager import DatabaseManager

class AnomalyDetector:
    def __init__(self):
        self.db = DatabaseManager()

    # Look for weird stats
    def detect_anomalies(self, player_uid):
        stats = self.db.get_player_stats(player_uid)
        if not stats:
            return None

        _, _, kills, deaths, headshots, damage, matches_played, _ = stats

        # Basic stats
        kdr = kills / deaths if deaths > 0 else kills
        hs_ratio = headshots / kills if kills > 0 else 0
        dpm = damage / matches_played if matches_played > 0 else 0

        # What looks suspicious
        KDR_THRESHOLD = 5.0
        HS_RATIO_THRESHOLD = 0.5
        DPM_THRESHOLD = 2000

        anomalies = []
        if kdr > KDR_THRESHOLD:
            anomalies.append(f"High KDR: {kdr:.2f}")
        if hs_ratio > HS_RATIO_THRESHOLD:
            anomalies.append(f"High headshot ratio: {hs_ratio:.2f}")
        if dpm > DPM_THRESHOLD:
            anomalies.append(f"High damage per match: {dpm:.0f}")

        return {
            'anomalies': anomalies,
            'metrics': {
                'kdr': kdr,
                'headshot_ratio': hs_ratio,
                'damage_per_match': dpm
            }
        }

# Main analysis function
def analyze_player(player_stats):
    try:
        total_stats = player_stats.get('total', {})
        global_stats = player_stats.get('global', {})
        
        # Get career stats
        total_kills = total_stats.get('specialEvent_kills', {}).get('value', 0)
        total_damage = total_stats.get('specialEvent_damage', {}).get('value', 0)
        total_wins = total_stats.get('specialEvent_wins', {}).get('value', 0)
        
        # Player info
        level = global_stats.get('level', 0)
        player_name = global_stats.get('name', '')
        
        # Rank stuff
        rank_info = global_stats.get('rank', {})
        rank_name = rank_info.get('rankName', 'Unknown')
        rank_div = rank_info.get('rankDiv', 0)
        rank_score = rank_info.get('rankScore', 0)
        
        # Estimate matches
        AVG_MATCHES_PER_LEVEL = 3
        estimated_matches = max(1, level * AVG_MATCHES_PER_LEVEL)
        
        # Calculate stats
        kdr = total_kills / estimated_matches if estimated_matches > 0 else 0
        dpm = total_damage / estimated_matches if estimated_matches > 0 else 0
        win_rate = (total_wins / estimated_matches * 100) if estimated_matches > 0 else 0
        avg_damage_per_kill = total_damage / total_kills if total_kills > 0 else 0
        
        # Suspicious thresholds
        KDR_THRESHOLD = 5.0
        DPM_THRESHOLD = 2000
        WIN_RATE_THRESHOLD = 30.0
        DAMAGE_PER_KILL_THRESHOLD = 300
        
        # Check for suspicious stuff
        suspicion_score = 0
        suspicious_indicators = []
        
        if kdr > KDR_THRESHOLD:
            suspicion_score += 25
            suspicious_indicators.append(f"High KDR: {kdr:.2f}")
        
        if dpm > DPM_THRESHOLD:
            suspicion_score += 25
            suspicious_indicators.append(f"High damage per match: {dpm:.0f}")
            
        if win_rate > WIN_RATE_THRESHOLD:
            suspicion_score += 25
            suspicious_indicators.append(f"High win rate: {win_rate:.1f}%")
            
        if avg_damage_per_kill > DAMAGE_PER_KILL_THRESHOLD:
            suspicion_score += 25
            suspicious_indicators.append(f"High damage per kill: {avg_damage_per_kill:.0f}")
            
        return {
            'name': player_name,
            'level': level,
            'total_kills': total_kills,
            'total_damage': total_damage,
            'total_wins': total_wins,
            'estimated_matches': estimated_matches,
            'kdr': kdr,
            'headshot_ratio': 0,  # No headshot data yet
            'dpm': dpm,
            'win_rate': win_rate,
            'avg_damage_per_kill': avg_damage_per_kill,
            'rank': f"{rank_name} {rank_div}" if rank_div > 0 else rank_name,
            'rank_score': rank_score,
            'suspicious_indicators': suspicious_indicators,
            'confidence_score': suspicion_score
        }
    except Exception as e:
        print(f"Error analyzing player data: {str(e)}")
        return None

# Print results
def print_analysis(player_name, results):
    if results is None:
        print(f"\nUnable to analyze {player_name} due to insufficient or invalid data.")
        return
        
    print(f"\nAnalysis for {player_name} ({results['name']}):")
    print(f"Level: {results['level']}")
    print(f"\nCareer Statistics:")
    print(f"  - Total Kills: {results['total_kills']:,}")
    print(f"  - Total Damage: {results['total_damage']:,}")
    print(f"  - Total Wins: {results['total_wins']:,}")
    print(f"  - Estimated Matches: {results['estimated_matches']:,}")
    
    print(f"\nPerformance Metrics:")
    print(f"  - KDR: {results['kdr']:.2f}")
    print(f"  - Damage per Match: {results['dpm']:.0f}")
    print(f"  - Win Rate: {results['win_rate']:.1f}%")
    print(f"  - Average Damage per Kill: {results['avg_damage_per_kill']:.0f}")
    print(f"  - Rank: {results['rank']} (Score: {results['rank_score']})")
    
    if results['suspicious_indicators']:
        print("\nSuspicious Activity Detected:")
        for indicator in results['suspicious_indicators']:
            print(f"- {indicator}")
        print(f"Confidence Score: {results['confidence_score']:.2f}%")
    else:
        print("\nNo suspicious activity detected.") 