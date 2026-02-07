"""Google Sheets client for fetching form responses."""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from config import GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_PATH, COLUMN_MAPPING


class SheetsClient:
    """Client for interacting with Google Sheets."""

    def __init__(self):
        """Initialize the Google Sheets client."""
        self.sheet_id = GOOGLE_SHEET_ID
        self.credentials_path = GOOGLE_CREDENTIALS_PATH
        self.client = None
        self.worksheet = None

    def connect(self):
        """Establish connection to Google Sheets."""
        try:
            # Define the scope
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]

            # Authenticate
            creds = Credentials.from_service_account_file(
                self.credentials_path, scopes=scope
            )
            self.client = gspread.authorize(creds)

            # Open the spreadsheet
            spreadsheet = self.client.open_by_key(self.sheet_id)

            # Get the first worksheet (you can change this to specific sheet name)
            self.worksheet = spreadsheet.get_worksheet(0)

            print(f"✅ Connected to Google Sheets: {spreadsheet.title}")
            return True

        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {e}")
            raise

    def get_all_data(self) -> pd.DataFrame:
        """Fetch all data from the sheet and return as DataFrame."""
        if not self.worksheet:
            self.connect()

        # Get all records as list of dictionaries
        records = self.worksheet.get_all_records()

        if not records:
            raise ValueError("No data found in the sheet")

        # Convert to DataFrame
        df = pd.DataFrame(records)

        # Rename columns using mapping
        df = df.rename(columns=COLUMN_MAPPING)

        # Parse timestamp
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        return df

    def get_weekly_data(self, weeks_ago: int = 0) -> pd.DataFrame:
        """
        Get data for a specific week.

        Args:
            weeks_ago: Number of weeks back from current week (0 = current week)

        Returns:
            DataFrame with filtered data for that week
        """
        df = self.get_all_data()

        # Calculate date range for the week
        today = datetime.now()
        start_of_current_week = today - timedelta(days=today.weekday())  # Monday
        start_of_target_week = start_of_current_week - timedelta(weeks=weeks_ago)
        end_of_target_week = start_of_target_week + timedelta(days=6)  # Sunday

        # Filter data for the week
        mask = (df["timestamp"] >= start_of_target_week) & (
            df["timestamp"] <= end_of_target_week
        )
        weekly_df = df[mask].copy()

        print(
            f"📅 Data for week: {start_of_target_week.date()} to {end_of_target_week.date()}"
        )
        print(f"📊 Found {len(weekly_df)} entries")

        return weekly_df

    def get_date_range_data(
        self, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Get data for a specific date range.

        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)

        Returns:
            DataFrame with filtered data
        """
        df = self.get_all_data()
        mask = (df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)
        return df[mask].copy()

    def get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics from the data."""
        if df.empty:
            return {}

        stats = {
            "total_entries": len(df),
            "date_range": {
                "start": df["timestamp"].min(),
                "end": df["timestamp"].max(),
            },
            "unique_days": df["day"].nunique() if "day" in df.columns else 0,
        }

        return stats


def test_connection():
    """Test function to verify connection and data fetching."""
    try:
        client = SheetsClient()
        client.connect()

        # Get all data
        df = client.get_all_data()
        print(f"\n📊 Total records: {len(df)}")
        print(f"📅 Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print(f"\n📝 Columns: {list(df.columns)}")
        print(f"\n🔍 First few rows:")
        print(df.head())

        # Get current week data
        weekly_df = client.get_weekly_data(weeks_ago=0)
        print(f"\n📅 Current week entries: {len(weekly_df)}")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()
