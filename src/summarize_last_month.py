"""Generate monthly summary and send via WhatsApp or Telegram (.env: NOTIFY_CHANNEL)."""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

# Add src to path if needed
sys.path.insert(0, str(Path(__file__).parent))

from sheets_client import SheetsClient
from analyzer import PersonalizationAnalyzer
import config


def get_last_month_data():
    """Last 30 calendar days ending at min(today, latest sheet date)."""
    print("📊 Fetching data from Google Sheets...")

    sheets_client = SheetsClient()
    sheets_client.connect()

    df = sheets_client.get_all_data()

    if df.empty:
        print("❌ No data found in the sheet")
        return None

    if "timestamp" not in df.columns:
        last_month = df.tail(30).copy()
        print(f"✅ Found {len(last_month)} entries (no timestamp; using last 30 rows)")
        return last_month

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    if df.empty:
        print("❌ No rows with valid timestamps")
        return None

    end_ts = min(pd.Timestamp.now(), df["timestamp"].max())
    end = end_ts.normalize()
    start = end - pd.Timedelta(days=29)
    mask = (df["timestamp"].dt.normalize() >= start) & (
        df["timestamp"].dt.normalize() <= end
    )
    last_month = df.loc[mask].sort_values("timestamp").copy()

    if last_month.empty:
        last_month = df.tail(30).copy()
        print("⚠️ No rows in last 30 calendar days; using last 30 sheet rows")

    print(f"✅ Found {len(last_month)} entries for analysis")

    if len(last_month) > 0:
        start_date = last_month["timestamp"].min()
        end_date = last_month["timestamp"].max()
        print(f"📅 Data range: {start_date.date()} to {end_date.date()}")

    return last_month


def generate_detailed_monthly_summary(df):
    """Concise monthly report (same structure as weekly, days logged X/30)."""
    print("\n🔍 Analyzing your monthly performance...")
    if df.empty:
        return "❌ No data available for monthly analysis"
    analyzer = PersonalizationAnalyzer(df)
    return analyzer.generate_monthly_report(period_days=30)


def send_notification(report):
    """Send the monthly summary via NOTIFY_CHANNEL (whatsapp or telegram)."""
    label = "Telegram" if config.NOTIFY_CHANNEL == "telegram" else "WhatsApp"
    print(f"\n📱 Sending monthly report to {label}...")

    client = config.get_notification_client()

    split_threshold = 4000 if config.NOTIFY_CHANNEL == "telegram" else 1600
    max_body = 3900 if config.NOTIFY_CHANNEL == "telegram" else 1500

    if len(report) > split_threshold:
        print("⚠️ Report is long, sending in parts...")

        parts = []
        lines = report.split("\n")
        current_part = []
        current_length = 0

        for line in lines:
            if current_length + len(line) + 1 > max_body:
                parts.append("\n".join(current_part))
                current_part = [line]
                current_length = len(line)
            else:
                current_part.append(line)
                current_length += len(line) + 1

        if current_part:
            parts.append("\n".join(current_part))

        success = True
        for i, part in enumerate(parts, 1):
            print(f"Sending part {i}/{len(parts)}...")
            message = f"📊 Monthly Report (Part {i}/{len(parts)})\n\n{part}"
            if not client.send_message(message):
                success = False
                break

        return success
    return client.send_monthly_report(report)


def main():
    """Main function to generate monthly summary."""
    print("=" * 70)
    print("🎯 Alpha-X - Monthly Performance Summary")
    print("=" * 70)
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    try:
        print("🔍 Validating configuration...")
        config.validate_config()
        print("✅ Configuration valid\n")

        df = get_last_month_data()

        if df is None or df.empty:
            print("\n❌ No data available. Please fill your daily form!")
            return

        report = generate_detailed_monthly_summary(df)

        print("\n" + "=" * 70)
        print("📊 YOUR MONTHLY PERFORMANCE SUMMARY")
        print("=" * 70)
        print(report)
        print("=" * 70)

        success = send_notification(report)

        if success:
            dest = "Telegram" if config.NOTIFY_CHANNEL == "telegram" else "WhatsApp"
            print(f"\n✨ Done! Check {dest} for the monthly summary.")
        else:
            print("\n⚠️ Summary generated but failed to send the notification.")
            print("Check NOTIFY_CHANNEL and Twilio or Telegram settings in .env.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
