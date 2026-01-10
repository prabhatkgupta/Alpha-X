"""Generate detailed monthly summary and send to WhatsApp."""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path if needed
sys.path.insert(0, str(Path(__file__).parent))

from sheets_client import SheetsClient
from analyzer import PersonalizationAnalyzer
from whatsapp_client import WhatsAppClient
import config
import pandas as pd


def get_last_month_data():
    """Fetch the last 30 days of data from the Google Sheet."""
    print("📊 Fetching data from Google Sheets...")

    sheets_client = SheetsClient()
    sheets_client.connect()

    # Get all data
    df = sheets_client.get_all_data()

    if df.empty:
        print("❌ No data found in the sheet")
        return None

    # Get last 30 days of data
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)

    # Filter data for last 30 days
    if "timestamp" in df.columns:
        mask = df["timestamp"] >= thirty_days_ago
        last_month = df[mask].copy()
    else:
        # If no timestamp, just get last 30 rows
        last_month = df.tail(30).copy()

    print(f"✅ Found {len(last_month)} entries for analysis")

    # Show date range
    if "timestamp" in last_month.columns and len(last_month) > 0:
        start_date = last_month["timestamp"].min()
        end_date = last_month["timestamp"].max()
        print(f"📅 Data range: {start_date.date()} to {end_date.date()}")

    return last_month


def calculate_trends(df):
    """Calculate week-over-week trends for the month."""
    if len(df) < 7:
        return None

    trends = {}

    # Split into weeks
    df_sorted = df.sort_values("timestamp") if "timestamp" in df.columns else df
    week1 = df_sorted.head(7)
    week4 = df_sorted.tail(7)

    # Career: Coding days trend
    if "coding" in df.columns:
        week1_coding = (week1["coding"] == "Yes").sum()
        week4_coding = (week4["coding"] == "Yes").sum()
        trends["coding"] = {
            "start": week1_coding,
            "end": week4_coding,
            "change": week4_coding - week1_coding,
        }

    # Health: Protein intake trend
    if "protein" in df.columns:
        week1_protein = (week1["protein"] == ">= 100g").sum()
        week4_protein = (week4["protein"] == ">= 100g").sum()
        trends["protein"] = {
            "start": week1_protein,
            "end": week4_protein,
            "change": week4_protein - week1_protein,
        }

    # Health: Workout trend
    if "workout" in df.columns:
        week1_workout = (week1["workout"] == "Yes").sum()
        week4_workout = (week4["workout"] == "Yes").sum()
        trends["workout"] = {
            "start": week1_workout,
            "end": week4_workout,
            "change": week4_workout - week1_workout,
        }

    return trends


def generate_detailed_monthly_summary(df):
    """Generate a comprehensive monthly summary with trends and insights."""
    print("\n🔍 Analyzing your monthly performance...")

    if df.empty:
        return "❌ No data available for monthly analysis"

    # Get date range
    if "timestamp" in df.columns:
        start_date = df["timestamp"].min()
        end_date = df["timestamp"].max()
        days_tracked = len(df)
    else:
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        days_tracked = len(df)

    # Basic weekly analysis
    analyzer = PersonalizationAnalyzer(df)

    # Calculate trends
    trends = calculate_trends(df)

    # Build detailed report
    report_lines = [
        f"📊 Monthly Performance Report",
        f"📅 {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}",
        f"📈 Days Tracked: {days_tracked}/30",
        "",
        "═" * 60,
        "",
    ]

    # === CAREER GROWTH SECTION ===
    career = analyzer.analyze_career()
    if career.get("has_data", False):
        report_lines.append("🎯 CAREER GROWTH (Priority #1)")
        report_lines.append("-" * 60)

    if "coding" in df.columns:
        coding_yes = (df["coding"] == "Yes").sum()
        coding_rate = (coding_yes / days_tracked) * 100

        if coding_rate >= 85:
            report_lines.append(
                f"✅ Coding: {coding_yes}/{days_tracked} days ({coding_rate:.0f}%) - Outstanding!"
            )
        elif coding_rate >= 70:
            report_lines.append(
                f"✅ Coding: {coding_yes}/{days_tracked} days ({coding_rate:.0f}%) - Good consistency"
            )
        else:
            report_lines.append(
                f"⚠️ Coding: {coding_yes}/{days_tracked} days ({coding_rate:.0f}%) - Needs improvement"
            )

        if trends and "coding" in trends:
            change = trends["coding"]["change"]
            if change > 0:
                report_lines.append(
                    f"📈 Trend: +{change} days from start to end of month (Improving!)"
                )
            elif change < 0:
                report_lines.append(
                    f"📉 Trend: {change} days from start to end of month (Declining)"
                )
            else:
                report_lines.append("➡️ Trend: Stable throughout the month")

    if "focus" in df.columns:
        sharp_days = (df["focus"] == "Good, razor sharp").sum()
        multitask_days = (df["focus"] == "I was multi-tasking, not good focus").sum()
        sharp_rate = (sharp_days / days_tracked) * 100

        report_lines.append(
            f"🎯 Focus: {sharp_days} days sharp ({sharp_rate:.0f}%), {multitask_days} days multi-tasking"
        )

        if sharp_days >= multitask_days:
            report_lines.append("💪 Focus quality trending positive!")
        else:
            report_lines.append("⚠️ Focus needs work - try time-blocking")

    if "career_focus" in df.columns:
        goal_achieved = (df["career_focus"] == "Good, achieved my today's goal").sum()
        lazy_days = (df["career_focus"] == "Lazy, didn't wanted to work").sum()
        report_lines.append(
            f"🏆 Goals: Achieved on {goal_achieved} days, {lazy_days} lazy days"
        )

    if career.get("has_data", False):
        report_lines.append("")

    # === HEALTH & FITNESS SECTION ===
    health = analyzer.analyze_health()
    if health.get("has_data", False):
        report_lines.append("💪 HEALTH & FITNESS (Priority #2)")
        report_lines.append("-" * 60)

    if "protein" in df.columns:
        protein_met = (df["protein"] == ">= 100g").sum()
        protein_rate = (protein_met / days_tracked) * 100
        report_lines.append(
            f"🍗 Protein: {protein_met}/{days_tracked} days ({protein_rate:.0f}%) met 100g target"
        )

        if trends and "protein" in trends:
            change = trends["protein"]["change"]
            if change > 0:
                report_lines.append(f"📈 Improved by {change} days from start to end!")

    if "workout" in df.columns:
        workout_days = (df["workout"] == "Yes").sum()
        workout_rate = (workout_days / days_tracked) * 100
        report_lines.append(
            f"🏋️ Workouts: {workout_days}/{days_tracked} days ({workout_rate:.0f}%)"
        )

        if trends and "workout" in trends:
            change = trends["workout"]["change"]
            if change > 0:
                report_lines.append(f"📈 Workout frequency increased by {change} days!")
            elif change < 0:
                report_lines.append(
                    f"📉 Workout frequency decreased by {abs(change)} days"
                )

    if "sleep" in df.columns:
        sleep_hours = []
        for val in df["sleep"]:
            if isinstance(val, str):
                import re

                match = re.search(r"(\d+)", val)
                if match:
                    sleep_hours.append(int(match.group(1)))

        if sleep_hours:
            avg_sleep = sum(sleep_hours) / len(sleep_hours)
            ideal_nights = sum(1 for h in sleep_hours if 7 <= h <= 8)
            report_lines.append(
                f"😴 Sleep: Avg {avg_sleep:.1f} hrs/night, {ideal_nights} nights in ideal range (7-8 hrs)"
            )

            if avg_sleep < 7:
                report_lines.append("⚠️ Sleep deficit detected - prioritize recovery!")

    if "sunshine" in df.columns:
        sunshine_days = (df["sunshine"] == "Yes").sum()
        sunshine_rate = (sunshine_days / days_tracked) * 100
        report_lines.append(
            f"☀️ Sunshine: {sunshine_days}/{days_tracked} days ({sunshine_rate:.0f}%)"
        )

    if health.get("has_data", False):
        report_lines.append("")

    # === MARRIAGE SECTION ===
    marriage = analyzer.analyze_marriage()
    if marriage.get("has_data", False):
        report_lines.append("❤️ MARRIAGE (Priority #3)")
        report_lines.append("-" * 60)

    if "marriage" in df.columns:
        good_days = (df["marriage"] == "Good").sum()
        okayish_days = (df["marriage"] == "Okayish").sum()
        not_good_days = (df["marriage"] == "Not good").sum()
        good_rate = (good_days / days_tracked) * 100

        report_lines.append(
            f"💑 Good: {good_days} days ({good_rate:.0f}%), Okayish: {okayish_days}, Not good: {not_good_days}"
        )

        if good_rate >= 70:
            report_lines.append("💝 Strong relationship focus this month!")
        elif good_rate >= 50:
            report_lines.append("💛 Moderate focus - room for improvement")
        else:
            report_lines.append("⚠️ Relationship needs more attention")

    if marriage.get("has_data", False):
        report_lines.append("")

    # === OVERALL PERFORMANCE ===
    report_lines.append("📈 OVERALL MONTHLY PERFORMANCE")
    report_lines.append("-" * 60)

    if "happiness" in df.columns:
        happy = (df["happiness"] == "Yes, I am happy").sum()
        neutral = (df["happiness"] == "Slightly Neutral, could do better").sum()
        bad = (df["happiness"] == "No, I performed bad").sum()
        happy_rate = (happy / days_tracked) * 100

        report_lines.append(
            f"😊 Happy Days: {happy}/{days_tracked} ({happy_rate:.0f}%)"
        )

        if happy_rate >= 70:
            report_lines.append("🎉 Great month overall!")
        elif happy_rate >= 50:
            report_lines.append("👍 Decent month, keep pushing!")
        else:
            report_lines.append("💪 Tough month, but you're tracking and improving!")

    if "performance" in df.columns:
        better = (df["performance"] == "Yes, better than yesterday").sum()
        worse = (df["performance"] == "Worst than yesterday").sum()
        better_rate = (better / days_tracked) * 100

        report_lines.append(
            f"📊 Better Days: {better} ({better_rate:.0f}%), Worse: {worse}"
        )

    if "day_overview" in df.columns:
        hard_enjoyed = (df["day_overview"] == "Did hard work - enjoyed").sum()
        procrastinated = (df["day_overview"] == "Procrastinated").sum()
        burnout = (df["day_overview"] == "Did hard work - burned out").sum()

        report_lines.append(
            f"💼 Work Quality: {hard_enjoyed} days enjoyed, {procrastinated} procrastinated, {burnout} burned out"
        )

    report_lines.append("")
    report_lines.append("═" * 60)
    report_lines.append("")

    # === KEY INSIGHTS ===
    report_lines.append("🎯 KEY MONTHLY INSIGHTS")
    report_lines.append("")

    # Top achievement
    achievements = []
    if (
        "protein" in df.columns
        and (df["protein"] == ">= 100g").sum() / days_tracked >= 0.8
    ):
        achievements.append("🏆 Protein target - consistently hit 100g!")
    if "workout" in df.columns and (df["workout"] == "Yes").sum() / days_tracked >= 0.7:
        achievements.append("🏆 Workout consistency - excellent dedication!")
    if "coding" in df.columns and (df["coding"] == "Yes").sum() / days_tracked >= 0.8:
        achievements.append("🏆 Coding discipline - great consistency!")

    if achievements:
        report_lines.append("✨ Top Achievements:")
        for achievement in achievements:
            report_lines.append(f"   {achievement}")
        report_lines.append("")

    # Areas for improvement
    improvements = []
    if "sleep" in df.columns:
        sleep_hours = [
            int(re.search(r"(\d+)", str(v)).group(1))
            for v in df["sleep"]
            if isinstance(v, str) and re.search(r"(\d+)", str(v))
        ]
        if sleep_hours and sum(sleep_hours) / len(sleep_hours) < 7:
            improvements.append("😴 Sleep - aim for 7-8 hours consistently")

    if "focus" in df.columns:
        if (df["focus"] == "I was multi-tasking, not good focus").sum() > (
            df["focus"] == "Good, razor sharp"
        ).sum():
            improvements.append("🎯 Focus - reduce multi-tasking, use time-blocking")

    if improvements:
        report_lines.append("💡 Focus Areas for Next Month:")
        for improvement in improvements:
            report_lines.append(f"   {improvement}")
        report_lines.append("")

    # Overall score - only from tracked areas
    tracked_sections = []
    if career.get("has_data", False):
        tracked_sections.append(career)
    if health.get("has_data", False):
        tracked_sections.append(health)
    if marriage.get("has_data", False):
        tracked_sections.append(marriage)

    if tracked_sections:
        total_score = sum(s.get("score", 0) for s in tracked_sections) / len(
            tracked_sections
        )
    else:
        total_score = 0

    # Add tracking summary
    report_lines.append(f"📋 Tracking {len(tracked_sections)} goal area(s) this month")
    report_lines.append("")

    if total_score >= 70:
        report_lines.append("🎉 EXCELLENT MONTH! Keep up the momentum!")
    elif total_score >= 50:
        report_lines.append("👍 SOLID MONTH! Small tweaks will make it great!")
    else:
        report_lines.append("💪 CHALLENGING MONTH! Every day is a new start!")

    report_lines.append("")
    report_lines.append("🚀 Next Month Goal: Build on strengths, improve weak areas!")

    import re

    return "\n".join(report_lines)


def send_to_whatsapp(report):
    """Send the monthly summary to WhatsApp."""
    print("\n📱 Sending monthly report to WhatsApp...")

    whatsapp_client = WhatsAppClient()

    # Monthly reports might be longer, so we might need to split
    if len(report) > 1600:
        print("⚠️ Report is long, sending in parts...")

        # Split into parts
        parts = []
        lines = report.split("\n")
        current_part = []
        current_length = 0

        for line in lines:
            if current_length + len(line) + 1 > 1500:  # Leave margin
                parts.append("\n".join(current_part))
                current_part = [line]
                current_length = len(line)
            else:
                current_part.append(line)
                current_length += len(line) + 1

        if current_part:
            parts.append("\n".join(current_part))

        # Send parts
        success = True
        for i, part in enumerate(parts, 1):
            print(f"Sending part {i}/{len(parts)}...")
            message = f"📊 Monthly Report (Part {i}/{len(parts)})\n\n{part}"
            if not whatsapp_client.send_message(message):
                success = False
                break

        return success
    else:
        return whatsapp_client.send_weekly_report(report)


def main():
    """Main function to generate monthly summary."""
    print("=" * 70)
    print("🎯 Alpha-X - Monthly Performance Summary")
    print("=" * 70)
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    try:
        # Validate configuration
        print("🔍 Validating configuration...")
        config.validate_config()
        print("✅ Configuration valid\n")

        # Step 1: Get last month data
        df = get_last_month_data()

        if df is None or df.empty:
            print("\n❌ No data available. Please fill your daily form!")
            return

        # Step 2: Generate detailed monthly summary
        report = generate_detailed_monthly_summary(df)

        # Display the report
        print("\n" + "=" * 70)
        print("📊 YOUR MONTHLY PERFORMANCE SUMMARY")
        print("=" * 70)
        print(report)
        print("=" * 70)

        # Step 3: Send to WhatsApp
        success = send_to_whatsapp(report)

        if success:
            print("\n✨ Done! Check your WhatsApp for the monthly summary.")
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
