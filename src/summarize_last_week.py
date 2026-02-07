"""Summarize last 7 days of data and send to WhatsApp."""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path if needed
sys.path.insert(0, str(Path(__file__).parent))

from sheets_client import SheetsClient
from analyzer import PersonalizationAnalyzer
from whatsapp_client import WhatsAppClient
import config


def get_last_7_days_data():
    """Fetch the last 7 rows from the Google Sheet."""
    print("📊 Fetching data from Google Sheets...")

    sheets_client = SheetsClient()
    sheets_client.connect()

    # Get all data
    df = sheets_client.get_all_data()

    if df.empty:
        print("❌ No data found in the sheet")
        return None

    # Get last 7 rows
    last_7_days = df.tail(7).copy()

    print(f"✅ Found {len(last_7_days)} entries for analysis")

    # Show date range
    if "timestamp" in last_7_days.columns:
        start_date = last_7_days["timestamp"].min()
        end_date = last_7_days["timestamp"].max()
        print(f"📅 Data range: {start_date.date()} to {end_date.date()}")

    return last_7_days


def generate_summary(df):
    """Generate a comprehensive summary of the last 7 days."""
    print("\n🔍 Analyzing your performance...")

    analyzer = PersonalizationAnalyzer(df)

    # Generate the report
    report = analyzer.generate_weekly_report()

    # Get focus areas
    focus_areas = analyzer.get_focus_areas()

    # Add focus areas to report if any
    if focus_areas:
        report += "\n\n🎯 Focus Areas for Next Week:"
        for i, area in enumerate(focus_areas, 1):
            report += f"\n   {i}. {area}"

    return report


def send_to_whatsapp(report):
    """Send the summary report to WhatsApp."""
    print("\n📱 Sending report to WhatsApp...")

    whatsapp_client = WhatsAppClient()
    success = whatsapp_client.send_weekly_report(report)

    if success:
        print("✅ Report sent successfully to WhatsApp!")
        return True
    else:
        print("❌ Failed to send report to WhatsApp")
        return False


def main():
    """Main function to summarize last 7 days and send to WhatsApp."""
    print("=" * 70)
    print("🎯 Alpha-X - Last 7 Days Summary")
    print("=" * 70)
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    try:
        # Validate configuration
        print("🔍 Validating configuration...")
        config.validate_config()
        print("✅ Configuration valid\n")

        # Step 1: Get last 7 days data
        df = get_last_7_days_data()

        if df is None or df.empty:
            print("\n❌ No data available. Please fill your daily form first!")
            return

        # Step 2: Generate summary
        report = generate_summary(df)

        # Display the report
        print("\n" + "=" * 70)
        print("📊 YOUR LAST 7 DAYS SUMMARY")
        print("=" * 70)
        print(report)
        print("=" * 70)

        # Step 3: Send to WhatsApp
        success = send_to_whatsapp(report)

        if success:
            print("\n✨ Done! Check your WhatsApp for the summary.")
        else:
            print("\n⚠️ Summary generated but failed to send to WhatsApp.")
            print("Check your Twilio credentials and try again.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
