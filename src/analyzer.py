"""Data analyzer for generating insights from daily tracking data."""

import re
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple, Optional
from collections import Counter

# Visible section breaks in Telegram/WhatsApp reports
SECTION_LINE = "━━━━━━━━━━━━━━━━━━━"

# Google Form "Day Overview ?" — must match linked sheet values exactly
DAY_OVERVIEW_EASY = "Did easy work"
DAY_OVERVIEW_HARD_ENJOYED = "Did hard work - enjoyed"
DAY_OVERVIEW_HARD_BURNED = "Did hard work - burned out"
DAY_OVERVIEW_PROCRASTINATED = "Procrastinated"


def _sleep_hours_from_cell(val) -> Optional[int]:
    if not isinstance(val, str):
        return None
    m = re.search(r"(\d+)", val)
    return int(m.group(1)) if m else None


class PersonalizationAnalyzer:
    """Analyzer for personal tracking data."""

    def __init__(self, df: pd.DataFrame):
        """Initialize analyzer with data."""
        self.df = df
        self.total_days = len(df)

    def analyze_career(self) -> Dict[str, Any]:
        """Analyze career growth metrics (Priority #1)."""
        analysis = {
            "priority": 1,
            "title": "🎯 CAREER GROWTH",
            "metrics": {},
            "insights": [],
            "score": 0,  # 0-100
            "has_data": False,
        }

        if self.df.empty:
            return analysis

        # Coding days
        if "coding" in self.df.columns:
            analysis["has_data"] = True
            coding_yes = (self.df["coding"] == "Yes").sum()
            coding_rate = coding_yes / self.total_days if self.total_days > 0 else 0
            analysis["metrics"]["coding_days"] = f"{coding_yes}/{self.total_days} days"

            if coding_rate >= 0.85:
                analysis["insights"].append(
                    f"✅ Coded {coding_yes}/{self.total_days} days - Excellent!"
                )
                analysis["score"] += 45
            elif coding_rate >= 0.7:
                analysis["insights"].append(
                    f"✅ Coded {coding_yes}/{self.total_days} days - Good!"
                )
                analysis["score"] += 35
            else:
                analysis["insights"].append(
                    f"⚠️ Only coded {coding_yes}/{self.total_days} days - Need more consistency"
                )
                analysis["score"] += 15

        # Career focus (daily career goal — not "focus quality"; see Focus section in reports)
        if "career_focus" in self.df.columns:
            analysis["has_data"] = True
            career_counts = self.df["career_focus"].value_counts()
            good_days = career_counts.get("Good, achieved my today's goal", 0)
            lazy_days = career_counts.get("Lazy, didn't wanted to work", 0)

            if good_days >= 5:
                analysis["insights"].append(
                    f"✅ Achieved daily goals {good_days} days - Fantastic!"
                )
                analysis["score"] += 45
            elif lazy_days >= 3:
                analysis["insights"].append(
                    f"⚠️ {lazy_days} lazy days - Let's fix this!"
                )
                analysis["insights"].append("💡 Tip: Break goals into smaller tasks")
                analysis["score"] += 15
            else:
                analysis["score"] += 25

        # If no career data at all
        if not analysis["has_data"]:
            analysis["insights"].append("ℹ️ No career tracking data found in your sheet")

        return analysis

    def analyze_health(self) -> Dict[str, Any]:
        """Analyze health & fitness metrics (Priority #2)."""
        analysis = {
            "priority": 2,
            "title": "💪 HEALTH & FITNESS",
            "metrics": {},
            "insights": [],
            "score": 0,
            "has_data": False,
        }

        if self.df.empty:
            return analysis

        # Protein intake
        if "protein" in self.df.columns:
            analysis["has_data"] = True
            protein_met = (self.df["protein"] == ">= 100g").sum()
            protein_rate = protein_met / self.total_days if self.total_days > 0 else 0
            analysis["metrics"]["protein"] = f"{protein_met}/{self.total_days} days"

            if protein_rate >= 0.85:
                analysis["insights"].append(
                    f"✅ Protein: {protein_met}/{self.total_days} days >= 100g - Excellent!"
                )
                analysis["score"] += 25
            elif protein_rate >= 0.6:
                analysis["insights"].append(
                    f"✅ Protein: {protein_met}/{self.total_days} days >= 100g - Good!"
                )
                analysis["score"] += 15
            else:
                analysis["insights"].append(
                    f"⚠️ Protein: Only {protein_met}/{self.total_days} days >= 100g"
                )
                analysis["insights"].append(
                    "💡 Tip: Prep protein-rich meals in advance"
                )
                analysis["score"] += 5

        # Workout
        if "workout" in self.df.columns:
            analysis["has_data"] = True
            workout_days = (self.df["workout"] == "Yes").sum()
            workout_rate = workout_days / self.total_days if self.total_days > 0 else 0
            analysis["metrics"]["workout"] = f"{workout_days}/{self.total_days} days"

            if workout_rate >= 0.7:
                analysis["insights"].append(
                    f"✅ Workout: {workout_days}/{self.total_days} days - Great consistency!"
                )
                analysis["score"] += 25
            elif workout_rate >= 0.5:
                analysis["insights"].append(
                    f"⚠️ Workout: {workout_days}/{self.total_days} days - Could be better"
                )
                analysis["score"] += 15
            else:
                analysis["insights"].append(
                    f"⚠️ Workout: Only {workout_days}/{self.total_days} days"
                )
                analysis["insights"].append("💡 Tip: Start with 20-min daily workouts")
                analysis["score"] += 5

        # Sleep analysis
        if "sleep" in self.df.columns:
            analysis["has_data"] = True
            sleep_hours = []
            for val in self.df["sleep"]:
                h = _sleep_hours_from_cell(val)
                if h is not None:
                    sleep_hours.append(h)

            if sleep_hours:
                avg_sleep = sum(sleep_hours) / len(sleep_hours)
                analysis["metrics"]["avg_sleep"] = f"{avg_sleep:.1f} hrs"

                if avg_sleep >= 7 and avg_sleep <= 9:
                    analysis["insights"].append(
                        f"✅ Sleep: Avg {avg_sleep:.1f} hrs - Perfect!"
                    )
                    analysis["score"] += 25
                elif avg_sleep >= 6:
                    analysis["insights"].append(
                        f"⚠️ Sleep: Avg {avg_sleep:.1f} hrs (Target: 7-8 hrs)"
                    )
                    analysis["insights"].append(
                        "💡 Tip: Sleep earlier for better recovery"
                    )
                    analysis["score"] += 15
                else:
                    analysis["insights"].append(
                        f"⚠️ Sleep: Avg {avg_sleep:.1f} hrs - Too low!"
                    )
                    analysis["insights"].append(
                        "💡 Tip: Prioritize sleep - it affects everything"
                    )
                    analysis["score"] += 5

        # Sunshine
        if "sunshine" in self.df.columns:
            analysis["has_data"] = True
            sunshine_days = (self.df["sunshine"] == "Yes").sum()
            if sunshine_days >= 5:
                analysis["insights"].append(
                    f"✅ Sunshine: {sunshine_days}/{self.total_days} days - Good!"
                )
                analysis["score"] += 25
            else:
                analysis["insights"].append(
                    f"⚠️ Sunshine: {sunshine_days}/{self.total_days} days"
                )
                analysis["insights"].append(
                    "💡 Tip: Morning sun boosts vitamin D & mood"
                )

        # Chewing gum
        if "chewing_gum" in self.df.columns:
            analysis["has_data"] = True
            gum_yes = (self.df["chewing_gum"].astype(str).str.strip().str.lower() == "yes").sum()
            analysis["metrics"]["chewing_gum"] = f"{gum_yes}/{self.total_days}"
            if gum_yes >= self.total_days * 0.7:
                analysis["insights"].append(
                    f"✅ Chewing gum: {gum_yes}/{self.total_days} days"
                )
                analysis["score"] += 10
            elif gum_yes > 0:
                analysis["insights"].append(
                    f"Chewing gum: {gum_yes}/{self.total_days} days"
                )
                analysis["score"] += 5

        # If no health data at all
        if not analysis["has_data"]:
            analysis["insights"].append(
                "ℹ️ No health/fitness tracking data found in your sheet"
            )

        return analysis

    def analyze_marriage(self) -> Dict[str, Any]:
        """Analyze marriage goals (Priority #3)."""
        analysis = {
            "priority": 3,
            "title": "❤️ MARRIAGE",
            "metrics": {},
            "insights": [],
            "score": 0,
            "has_data": False,
        }

        if self.df.empty or "marriage" not in self.df.columns:
            analysis["insights"].append("ℹ️ Not tracking marriage/relationship data")
            return analysis

        analysis["has_data"] = True

        marriage_counts = self.df["marriage"].value_counts()
        good_days = marriage_counts.get("Good", 0)
        okayish_days = marriage_counts.get("Okayish", 0)
        not_good_days = marriage_counts.get("Not good", 0)

        analysis["metrics"][
            "status"
        ] = f"Good: {good_days}, Okayish: {okayish_days}, Not good: {not_good_days}"

        good_rate = good_days / self.total_days if self.total_days > 0 else 0

        if good_rate >= 0.7:
            analysis["insights"].append(
                f"✅ Strong relationship focus: {good_days}/{self.total_days} good days"
            )
            analysis["score"] = 100
        elif good_rate >= 0.4:
            analysis["insights"].append(
                f"⚠️ Moderate performance: {good_days} good, {okayish_days} okayish days"
            )
            analysis["insights"].append("💡 Tip: Schedule quality time together")
            analysis["score"] = 60
        else:
            analysis["insights"].append(
                f"⚠️ Needs attention: {not_good_days} not good days"
            )
            analysis["insights"].append(
                "💡 Tip: Have an open conversation about expectations"
            )
            analysis["score"] = 30

        return analysis

    def analyze_overall_performance(self) -> Dict[str, Any]:
        """Analyze overall performance and happiness."""
        analysis = {"title": "📈 OVERALL PERFORMANCE", "metrics": {}, "insights": []}

        if self.df.empty:
            return analysis

        # Performance trend
        if "performance" in self.df.columns:
            perf_counts = self.df["performance"].value_counts()
            better = perf_counts.get("Yes, better than yesterday", 0)
            same = perf_counts.get("Same as yesterday", 0)
            worse = perf_counts.get("Worst than yesterday", 0)

            if better >= worse:
                analysis["insights"].append(
                    f"Week Trend: Better than yesterday on {better}/{self.total_days} days 🎉"
                )
            else:
                analysis["insights"].append(
                    f"Week Trend: {worse} worse days - Let's turn this around"
                )

        # Happiness
        if "happiness" in self.df.columns:
            happy_counts = self.df["happiness"].value_counts()
            happy = happy_counts.get("Yes, I am happy", 0)
            neutral = happy_counts.get("Slightly Neutral, could do better", 0)
            bad = happy_counts.get("No, I performed bad", 0)

            analysis["metrics"]["happy_days"] = f"{happy}/{self.total_days} days"

            if happy >= 5:
                analysis["insights"].append(
                    f"Happy Days: {happy}/{self.total_days} days - Great! 😊"
                )
            elif happy >= 3:
                analysis["insights"].append(
                    f"Happy Days: {happy}/{self.total_days} days - Keep going! 💪"
                )
            else:
                analysis["insights"].append(
                    f"Happy Days: Only {happy}/{self.total_days} days"
                )
                analysis["insights"].append("💡 Remember: Progress > Perfection")

        # Day overview
        if "day_overview" in self.df.columns:
            overview_counts = self.df["day_overview"].value_counts()
            hard_enjoyed = overview_counts.get(DAY_OVERVIEW_HARD_ENJOYED, 0)
            procrastinated = overview_counts.get(DAY_OVERVIEW_PROCRASTINATED, 0)
            easy_days = overview_counts.get(DAY_OVERVIEW_EASY, 0)

            if hard_enjoyed >= 4:
                analysis["insights"].append(
                    f"🌟 This Week's Win: Did hard work & enjoyed it {hard_enjoyed} days!"
                )
            if easy_days >= 4:
                analysis["insights"].append(
                    f"📗 Easy days: {easy_days} — ok for recovery; balance with harder focus when ready"
                )
            if procrastinated >= 3:
                analysis["insights"].append(
                    f"⚠️ Procrastinated {procrastinated} days - Break tasks smaller"
                )

        return analysis

    @staticmethod
    def days_logged_ratio(df: pd.DataFrame, period_days: int) -> Tuple[int, int]:
        """Distinct calendar days with an entry vs period length (e.g. 7 or 30)."""
        if df.empty or period_days <= 0:
            return (0, max(period_days, 0))
        if "timestamp" in df.columns and df["timestamp"].notna().any():
            ts = pd.to_datetime(df["timestamp"], errors="coerce").dropna()
            if ts.empty:
                return (0, period_days)
            uniq = int(ts.dt.normalize().nunique())
            return (min(uniq, period_days), period_days)
        return (min(len(df), period_days), period_days)

    def _n(self) -> int:
        return max(self.total_days, 1)

    def _career_lines(self) -> List[str]:
        df, n = self.df, self._n()
        lines: List[str] = []
        if "career_focus" in df.columns:
            good = (df["career_focus"] == "Good, achieved my today's goal").sum()
            lazy = (df["career_focus"] == "Lazy, didn't wanted to work").sum()
            lines.append(f"• Career focus: {good}/{n} on goal, {lazy} low")
        if "coding" in df.columns:
            cy = (df["coding"] == "Yes").sum()
            lines.append(f"• Code ≥1h: {cy}/{n}")
        return lines

    def _health_lines(self) -> List[str]:
        df, n = self.df, self._n()
        lines: List[str] = []
        if "workout" in df.columns:
            w = (df["workout"] == "Yes").sum()
            lines.append(f"• Workout: {w}/{n}")
        if "sunshine" in df.columns:
            s = (df["sunshine"] == "Yes").sum()
            lines.append(f"• Sunshine 15m: {s}/{n}")
        if "protein" in df.columns:
            p = (df["protein"] == ">= 100g").sum()
            lines.append(f"• Protein ≥100g: {p}/{n}")
        if "sleep" in df.columns:
            hrs = [_sleep_hours_from_cell(v) for v in df["sleep"]]
            hrs = [h for h in hrs if h is not None]
            if hrs:
                ge7 = sum(1 for h in hrs if h >= 7)
                avg = sum(hrs) / len(hrs)
                lines.append(f"• Sleep ≥7h: {ge7}/{len(hrs)} nights (avg {avg:.1f}h)")
        if "chewing_gum" in df.columns:
            g = (df["chewing_gum"].astype(str).str.strip().str.lower() == "yes").sum()
            lines.append(f"• Chewing gum: {g}/{n}")
        return lines

    def _focus_lines(self) -> List[str]:
        df, n = self.df, self._n()
        lines: List[str] = []
        if "focus" in df.columns:
            sharp = (df["focus"] == "Good, razor sharp").sum()
            multi = (df["focus"] == "I was multi-tasking, not good focus").sum()
            lines.append(f"• Focus sharp: {sharp}/{n} · multitask: {multi}/{n}")
        if "day_overview" in df.columns:
            easy = (df["day_overview"] == DAY_OVERVIEW_EASY).sum()
            hard = (df["day_overview"] == DAY_OVERVIEW_HARD_ENJOYED).sum()
            burn = (df["day_overview"] == DAY_OVERVIEW_HARD_BURNED).sum()
            proc = (df["day_overview"] == DAY_OVERVIEW_PROCRASTINATED).sum()
            lines.append(
                f"• Day: easy {easy} · hard+enjoyed {hard} · burned {burn} · procrastinated {proc}"
            )
        return lines

    def _happy_misc_lines(self) -> List[str]:
        df, n = self.df, self._n()
        lines: List[str] = []
        if "happiness" in df.columns:
            happy = (df["happiness"] == "Yes, I am happy").sum()
            lines.append(f"• Happy w/ performance: {happy}/{n}")
        if "marriage" in df.columns:
            g = (df["marriage"] == "Good").sum()
            ok = (df["marriage"] == "Okayish").sum()
            bad = (df["marriage"] == "Not good").sum()
            lines.append(f"• Marriage: good {g} · ok {ok} · not good {bad}")
        if "performance" in df.columns:
            b = (df["performance"] == "Yes, better than yesterday").sum()
            w = (df["performance"] == "Worst than yesterday").sum()
            lines.append(f"• vs yesterday: better {b} · worse {w}")
        return lines

    def _append_section(
        self, lines: List[str], title: str, body: List[str]
    ) -> None:
        if not body:
            return
        lines.append(SECTION_LINE)
        lines.append(title)
        lines.append(SECTION_LINE)
        lines.extend(body)
        # Extra blank line between sections (join inserts \n between each entry)
        lines.extend(["", ""])

    def _overall_one_liner(self) -> str:
        career = self.analyze_career()
        health = self.analyze_health()
        marriage = self.analyze_marriage()
        tracked = [
            s
            for s in (career, health, marriage)
            if s.get("has_data", False)
        ]
        if not tracked:
            return ""
        avg = sum(s["score"] for s in tracked) / len(tracked)
        if avg >= 70:
            return "🎉 Strong week on core goals."
        if avg >= 50:
            return "👍 Decent week — tighten the weak spots."
        return "💪 Rough week — pick one lever for next week."

    def generate_weekly_report(self) -> str:
        """Short weekly report: Career → Health → Focus → Happy & misc, with days logged X/7."""
        if self.df.empty:
            return "❌ No data available for this week"

        logged, period = self.days_logged_ratio(self.df, 7)
        ts = self.df["timestamp"] if "timestamp" in self.df.columns else None
        if ts is not None and ts.notna().any():
            start_date = pd.to_datetime(ts).min()
            end_date = pd.to_datetime(ts).max()
            hdr = f"📊 Weekly · {start_date.strftime('%b %d')}–{end_date.strftime('%b %d, %Y')}"
        else:
            hdr = "📊 Weekly report"

        lines = [
            hdr,
            f"📝 Days logged: {logged}/{period}",
            "",
        ]

        self._append_section(lines, "🎯 Career", self._career_lines())
        self._append_section(lines, "💪 Health", self._health_lines())
        self._append_section(lines, "🧠 Focus", self._focus_lines())
        self._append_section(lines, "😊 Happy & misc", self._happy_misc_lines())

        closing = self._overall_one_liner()
        if closing:
            lines.append(SECTION_LINE)
            lines.append(closing)

        return "\n".join(lines).strip()

    def generate_monthly_report(self, period_days: int = 30) -> str:
        """Concise monthly report with days logged X/30 and the same four sections."""
        if self.df.empty:
            return "❌ No data available for monthly analysis"

        logged, period = self.days_logged_ratio(self.df, period_days)
        ts = self.df["timestamp"] if "timestamp" in self.df.columns else None
        if ts is not None and ts.notna().any():
            start_date = pd.to_datetime(ts).min()
            end_date = pd.to_datetime(ts).max()
            hdr = f"📊 Monthly · {start_date.strftime('%b %d')} – {end_date.strftime('%b %d, %Y')}"
        else:
            hdr = "📊 Monthly report"

        lines = [
            hdr,
            f"📝 Days logged: {logged}/{period}",
            "",
        ]

        self._append_section(lines, "🎯 Career", self._career_lines())
        self._append_section(lines, "💪 Health", self._health_lines())
        self._append_section(lines, "🧠 Focus", self._focus_lines())
        self._append_section(lines, "😊 Happy & misc", self._happy_misc_lines())

        career = self.analyze_career()
        health = self.analyze_health()
        marriage = self.analyze_marriage()
        tracked = [s for s in (career, health, marriage) if s.get("has_data", False)]
        if tracked:
            avg = sum(s["score"] for s in tracked) / len(tracked)
            if avg >= 70:
                tag = "🎉 Solid month on core goals."
            elif avg >= 50:
                tag = "👍 OK month — push the gaps next month."
            else:
                tag = "💪 Hard month — reset and stack small wins."
            lines.append(SECTION_LINE)
            lines.append(tag)

        return "\n".join(lines).strip()

    def get_focus_areas(self) -> List[str]:
        """Top focus hints aligned with Career / Health / Focus / Happy & misc."""
        out: List[str] = []
        career = self.analyze_career()
        health = self.analyze_health()
        marriage = self.analyze_marriage()

        if career["score"] < 60:
            out.append("Career: code ≥1h more often + hit daily career goal")
        if health["score"] < 60:
            out.append(
                "Health: workout, sun, protein, sleep ≥7h, chewing gum habit"
            )
        df = self.df
        if "focus" in df.columns and "day_overview" in df.columns:
            sharp = (df["focus"] == "Good, razor sharp").sum()
            multi = (df["focus"] == "I was multi-tasking, not good focus").sum()
            proc = (df["day_overview"] == DAY_OVERVIEW_PROCRASTINATED).sum()
            if multi > sharp or proc >= 3:
                out.append("Focus: fewer tabs, time-blocks; reduce procrastination")
        if marriage["score"] < 60:
            out.append("Happy & misc: marriage + end-day happiness check-in")

        return out[:4]


if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        "timestamp": pd.date_range("2026-01-05", periods=7),
        "coding": ["Yes", "Yes", "No", "Yes", "Yes", "Yes", "No"],
        "focus": ["Good, razor sharp"] * 4
        + ["I was multi-tasking, not good focus"] * 3,
        "protein": [">= 100g"] * 6 + ["< 100g"],
        "workout": ["Yes"] * 5 + ["No"] * 2,
        "sleep": ["7 hrs", "6 hrs", "7 hrs", "8 hrs", "6 hrs", "7 hrs", "6 hrs"],
        "marriage": ["Good", "Okayish", "Good", "Okayish", "Good", "Good", "Okayish"],
        "happiness": ["Yes, I am happy"] * 5
        + ["Slightly Neutral, could do better"] * 2,
    }

    df = pd.DataFrame(sample_data)
    analyzer = PersonalizationAnalyzer(df)

    print(analyzer.generate_weekly_report())
