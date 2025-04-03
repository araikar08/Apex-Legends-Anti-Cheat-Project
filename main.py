from api.data_fetcher import DataFetcher
from analysis.player_analyzer import PlayerAnalyzer
from analysis.anomaly_detector import AnomalyDetector
from analysis.ml_analyzer import MLAnomalyDetector
from config import PLATFORMS
import argparse

def analyze_player(player_name, platform):
    fetcher = DataFetcher()
    analyzer = PlayerAnalyzer()
    detector = AnomalyDetector()
    ml_detector = MLAnomalyDetector()

    try:
        print(f"\nFetching data for {player_name}...")
        # Fetch and store player data
        result = fetcher.fetch_and_store_player_data(player_name, platform)
        player_uid = result['uid']
        print(f"Player UID: {player_uid}")
        print(f"Raw stats: {result['stats']}")

        # Analyze player
        print("\nAnalyzing player data...")
        analysis = analyzer.analyze_player(player_uid)
        if not analysis:
            print(f"Not enough data for {player_name}")
            return

        # Detect anomalies
        anomalies = detector.detect_anomalies(player_uid)
        
        # ML Analysis
        ml_results = ml_detector.detect_anomalies(analysis)

        # Print results
        print(f"\nAnalysis for {player_name}:")
        print(f"KDR: {analysis['kdr']:.2f}")
        print(f"Headshot Ratio: {analysis['headshot_ratio']:.2%}")
        print(f"Damage per Match: {analysis['damage_per_match']:.0f}")

        if analysis['suspicious']:
            print("\nSuspicious Activity Detected:")
            for reason in analysis['reasons']:
                print(f"- {reason}")
            print(f"Confidence Score: {analysis['confidence']:.2%}")

        if anomalies and anomalies['anomalies']:
            print("\nStatistical Anomalies Detected:")
            for anomaly in anomalies['anomalies']:
                print(f"- {anomaly}")
                
        if ml_results['is_anomaly']:
            print("\nML Analysis Results:")
            print(f"- ML Confidence Score: {ml_results['ml_confidence']:.2%}")
            print(f"- Normalized Features: {ml_results['features']}")

    except Exception as e:
        print(f"Error analyzing {player_name}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Apex Legends Player Analysis Tool')
    parser.add_argument('--player', help='Player name to analyze')
    parser.add_argument('--platform', choices=PLATFORMS.values(), help='Platform (PC, PS4, X1)')
    parser.add_argument('--file', help='File containing list of players (one per line)')
    args = parser.parse_args()

    if args.player and args.platform:
        analyze_player(args.player, args.platform)
    elif args.file:
        with open(args.file, 'r') as f:
            for line in f:
                name, platform = line.strip().split(',')
                analyze_player(name, platform)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 