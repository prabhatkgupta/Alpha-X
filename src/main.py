"""Main application entry point for Alpha-X."""

import argparse
from datetime import datetime
from sheets_client import SheetsClient
from analyzer import PersonalizationAnalyzer
from whatsapp_client import WhatsAppClient
import config


def main(weeks_ago: int = 0, dry_run: bool = False):
    """
    Main function to generate and send weekly insights.

    Args:
        weeks_ago: Number of weeks back to analyze (0 = current week)
        dry_run: If True, only print report without sending
    """
    print("=" * 60)
    print("🎯 Alpha-X - Weekly Insights Generator")
    print("=" * 60)
    print()

    try:
        # Validate configuration
        print("🔍 Validating configuration...")
        config.validate_config()
        print("✅ Configuration valid\n")

        # Connect to Google Sheets
        print("📊 Fetching data from Google Sheets...")
        sheets_client = SheetsClient()
        sheets_client.connect()

        # Get weekly data
        weekly_data = sheets_client.get_weekly_data(weeks_ago=weeks_ago)

        if weekly_data.empty:
            print("❌ No data found for the specified week")
            return

        print(f"✅ Found {len(weekly_data)} entries for analysis\n")

        # Analyze data
        print("🔍 Analyzing your performance...")
        analyzer = PersonalizationAnalyzer(weekly_data)
        report = analyzer.generate_weekly_report()

        print("\n" + "=" * 60)
        print("📊 WEEKLY REPORT")
        print("=" * 60)
        print(report)
        print("=" * 60)

        # Get focus areas
        focus_areas = analyzer.get_focus_areas()
        if focus_areas:
            print("\n🎯 Focus Areas for Next Week:")
            for i, area in enumerate(focus_areas, 1):
                print(f"   {i}. {area}")
            print()

        # Send via WhatsApp
        if not dry_run:
            print("\n📱 Sending report to WhatsApp...")
            whatsapp_client = WhatsAppClient()
            success = whatsapp_client.send_weekly_report(report)

            if success:
                print("✅ Report sent successfully!")
            else:
                print("❌ Failed to send report")
                return
        else:
            print("\n⚠️ Dry run mode - Report not sent")

        print("\n✨ Done!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and send weekly personalization insights"
    )
    parser.add_argument(
        "--weeks-ago",
        type=int,
        default=0,
        help="Number of weeks back to analyze (0 = current week, 1 = last week, etc.)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate report without sending to WhatsApp",
    )

    args = parser.parse_args()

    main(weeks_ago=args.weeks_ago, dry_run=args.dry_run)
