"""Configuration management for Alpha-X."""

import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_DIR = BASE_DIR / "credentials"

# Helper function to extract Sheet ID from URL
def extract_sheet_id_from_url(url):
    """Extract Google Sheet ID from a Google Sheets URL."""
    if not url:
        return None
    
    # Pattern: https://docs.google.com/spreadsheets/d/SHEET_ID/edit...
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    return None

# Google Sheets Configuration
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# If GOOGLE_SHEET_ID is not set, try to extract it from GOOGLE_SHEET_URL
if not GOOGLE_SHEET_ID and GOOGLE_SHEET_URL:
    GOOGLE_SHEET_ID = extract_sheet_id_from_url(GOOGLE_SHEET_URL)

GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL")  # Optional: Form URL for reference
GOOGLE_CREDENTIALS_PATH = CREDENTIALS_DIR / "google_sheets_credentials.json"

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")

# Goal Priorities
GOALS_PRIORITY = {
    1: "Career Growth",
    2: "Health & Fitness",
    3: "Marriage",
    4: "Investments Growth"
}

# Column mapping from Google Form to data fields
COLUMN_MAPPING = {
    "Timestamp": "timestamp",
    "Met Protein intake ?": "protein",
    "Day": "day",
    "Did you code more than 1 hour ?": "coding",
    "Marriage goals ?": "marriage",
    "Workout ?": "workout",
    "You did better overall ?": "performance",
    "15 mins sunshine ?": "sunshine",
    "Chewing Gum ?": "chewing_gum",
    "Are you happy today with your performance ?": "happiness",
    "Sleep": "sleep",
    "Day Overview ?": "day_overview",
    "How was your focus ?": "focus",
    "Focused on Career ?": "career_focus"
}

def validate_config():
    """Validate that all required configurations are set."""
    errors = []
    
    if not GOOGLE_SHEET_ID:
        if GOOGLE_SHEET_URL:
            errors.append("GOOGLE_SHEET_ID could not be extracted from GOOGLE_SHEET_URL. Please check the URL format.")
        else:
            errors.append("GOOGLE_SHEET_ID or GOOGLE_SHEET_URL must be set")
    
    if not GOOGLE_CREDENTIALS_PATH.exists():
        errors.append(f"Google credentials file not found at {GOOGLE_CREDENTIALS_PATH}")
    
    if not TWILIO_ACCOUNT_SID:
        errors.append("TWILIO_ACCOUNT_SID is not set")
    
    if not TWILIO_AUTH_TOKEN:
        errors.append("TWILIO_AUTH_TOKEN is not set")
    
    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
    
    print(f"✓ Using Google Sheet ID: {GOOGLE_SHEET_ID}")
    return True

if __name__ == "__main__":
    try:
        validate_config()
        print("✅ Configuration is valid!")
    except ValueError as e:
        print(f"❌ {e}")

