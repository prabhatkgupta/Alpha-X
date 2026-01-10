"""Scheduler for automated weekly reports."""

import schedule
import time
from datetime import datetime
from summarize_last_week import main as summarize_main


def send_weekly_summary():
    """Job function to send weekly summary of last 7 days."""
    print(f"\n⏰ Scheduled job triggered at {datetime.now()}")
    print("📊 Generating summary of last 7 days...")
    summarize_main()


def run_scheduler():
    """Run the scheduler for automated weekly summaries."""
    print("=" * 70)
    print("🤖 Alpha-X - Weekly Summary Scheduler")
    print("=" * 70)
    print()
    print("📅 Schedule: Every Sunday at 1:00 PM")
    print("📊 Action: Summarize last 7 days and send to WhatsApp")
    print("⏰ Current time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    print("💡 Tip: Run this in the background or as a system service")
    print("Press Ctrl+C to stop the scheduler")
    print("=" * 70)
    print()
    
    # Schedule: Every Sunday at 1:00 PM (13:00)
    schedule.every().sunday.at("13:00").do(send_weekly_summary)
    
    # For testing: uncomment to run every minute
    # schedule.every(1).minutes.do(send_weekly_summary)
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n⏹️ Scheduler stopped by user")


if __name__ == "__main__":
    run_scheduler()

