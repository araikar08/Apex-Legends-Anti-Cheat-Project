import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_KEY = os.getenv('APEX_API_KEY')
API_BASE_URL = 'https://api.mozambiquehe.re/'
RATE_LIMIT = 2  # requests per second

# Database Configuration
DB_PATH = 'database/apex_data.db'

# Analysis Configuration
SUSPICIOUS_KDR_THRESHOLD = 5.0
SUSPICIOUS_HEADSHOT_RATIO = 0.5
MIN_MATCHES_FOR_ANALYSIS = 10

# Platform Codes
PLATFORMS = {
    'PC': 'PC',
    'PS4': 'PS4',
    'XBOX': 'X1'
} 