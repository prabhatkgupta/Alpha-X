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
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
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

# Notifications: "whatsapp" (Twilio) or "telegram" (Bot API)
NOTIFY_CHANNEL = (os.getenv("NOTIFY_CHANNEL") or "whatsapp").strip().lower()

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")

# Telegram Bot API (https://core.telegram.org/bots/api)
_tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = _tg_token.strip() if _tg_token else None
_tg_chat = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_CHAT_ID = _tg_chat.strip() if _tg_chat else None

# Goal areas (order for reports)
GOALS_PRIORITY = {
    1: "Career",
    2: "Health",
    3: "Focus",
    4: "Happy & misc",
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
    "Focused on Career ?": "career_focus",
}


def validate_config():
    """Validate that all required configurations are set."""
    errors = []

    if not GOOGLE_SHEET_ID:
        if GOOGLE_SHEET_URL:
            errors.append(
                "GOOGLE_SHEET_ID could not be extracted from GOOGLE_SHEET_URL. Please check the URL format."
            )
        else:
            errors.append("GOOGLE_SHEET_ID or GOOGLE_SHEET_URL must be set")

    if not GOOGLE_CREDENTIALS_PATH.exists():
        errors.append(f"Google credentials file not found at {GOOGLE_CREDENTIALS_PATH}")

    if NOTIFY_CHANNEL not in ("whatsapp", "telegram"):
        errors.append(
            f"NOTIFY_CHANNEL must be 'whatsapp' or 'telegram', got: {NOTIFY_CHANNEL!r}"
        )

    if NOTIFY_CHANNEL == "whatsapp":
        if not TWILIO_ACCOUNT_SID:
            errors.append("TWILIO_ACCOUNT_SID is not set")
        if not TWILIO_AUTH_TOKEN:
            errors.append("TWILIO_AUTH_TOKEN is not set")
    elif NOTIFY_CHANNEL == "telegram":
        if not TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is not set")
        if not TELEGRAM_CHAT_ID:
            errors.append("TELEGRAM_CHAT_ID is not set (numeric id from @userinfobot or getUpdates)")

    if errors:
        raise ValueError(
            f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
        )

    print(f"✓ Using Google Sheet ID: {GOOGLE_SHEET_ID}")
    print(f"✓ Notifications: {NOTIFY_CHANNEL}")
    return True


def get_notification_client():
    """Return WhatsApp (Twilio) or Telegram client based on NOTIFY_CHANNEL."""
    if NOTIFY_CHANNEL == "telegram":
        from telegram_client import TelegramClient

        return TelegramClient()
    from whatsapp_client import WhatsAppClient

    return WhatsAppClient()


if __name__ == "__main__":
    try:
        validate_config()
        print("✅ Configuration is valid!")
    except ValueError as e:
        print(f"❌ {e}")
