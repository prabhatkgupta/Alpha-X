"""Unit tests for Alpha-X analyzer module."""

import pytest
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from analyzer import PersonalizationAnalyzer


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = {
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
        "performance": ["Yes, better than yesterday"] * 4 + ["Same as yesterday"] * 3,
        "day_overview": ["Did hard work - enjoyed"] * 5 + ["Procrastinated"] * 2,
        "career_focus": ["Good, achieved my today's goal"] * 5
        + ["Neutral, gave my best"] * 2,
        "sunshine": ["Yes"] * 6 + ["No"],
    }
    return pd.DataFrame(data)


def test_analyzer_initialization(sample_data):
    """Test analyzer initialization."""
    analyzer = PersonalizationAnalyzer(sample_data)
    assert analyzer.total_days == 7
    assert len(analyzer.df) == 7


def test_career_analysis(sample_data):
    """Test career growth analysis."""
    analyzer = PersonalizationAnalyzer(sample_data)
    career = analyzer.analyze_career()

    assert career["priority"] == 1
    assert career["title"] == "🎯 CAREER GROWTH"
    assert "metrics" in career
    assert "insights" in career
    assert "score" in career
    assert career["score"] > 0


def test_health_analysis(sample_data):
    """Test health & fitness analysis."""
    analyzer = PersonalizationAnalyzer(sample_data)
    health = analyzer.analyze_health()

    assert health["priority"] == 2
    assert health["title"] == "💪 HEALTH & FITNESS"
    assert "metrics" in health
    assert "insights" in health
    assert "score" in health


def test_marriage_analysis(sample_data):
    """Test marriage goals analysis."""
    analyzer = PersonalizationAnalyzer(sample_data)
    marriage = analyzer.analyze_marriage()

    assert marriage["priority"] == 3
    assert marriage["title"] == "❤️ MARRIAGE"
    assert "score" in marriage


def test_overall_performance(sample_data):
    """Test overall performance analysis."""
    analyzer = PersonalizationAnalyzer(sample_data)
    overall = analyzer.analyze_overall_performance()

    assert overall["title"] == "📈 OVERALL PERFORMANCE"
    assert "insights" in overall


def test_generate_weekly_report(sample_data):
    """Test weekly report generation."""
    analyzer = PersonalizationAnalyzer(sample_data)
    report = analyzer.generate_weekly_report()

    assert isinstance(report, str)
    assert len(report) > 0
    assert "📊 Weekly Report" in report
    assert "CAREER GROWTH" in report
    assert "HEALTH & FITNESS" in report


def test_focus_areas(sample_data):
    """Test focus areas identification."""
    analyzer = PersonalizationAnalyzer(sample_data)
    focus_areas = analyzer.get_focus_areas()

    assert isinstance(focus_areas, list)
    assert len(focus_areas) <= 3


def test_empty_dataframe():
    """Test analyzer with empty dataframe."""
    empty_df = pd.DataFrame()
    analyzer = PersonalizationAnalyzer(empty_df)

    report = analyzer.generate_weekly_report()
    assert "No data available" in report


def test_career_high_performance():
    """Test career analysis with high performance."""
    data = {
        "timestamp": pd.date_range("2026-01-05", periods=7),
        "coding": ["Yes"] * 7,
        "focus": ["Good, razor sharp"] * 7,
        "career_focus": ["Good, achieved my today's goal"] * 7,
    }
    df = pd.DataFrame(data)
    analyzer = PersonalizationAnalyzer(df)
    career = analyzer.analyze_career()

    assert career["score"] >= 80  # High score for excellent performance


def test_health_metrics():
    """Test health metrics calculation."""
    data = {
        "timestamp": pd.date_range("2026-01-05", periods=7),
        "protein": [">= 100g"] * 7,
        "workout": ["Yes"] * 7,
        "sleep": ["8 hrs"] * 7,
        "sunshine": ["Yes"] * 7,
    }
    df = pd.DataFrame(data)
    analyzer = PersonalizationAnalyzer(df)
    health = analyzer.analyze_health()

    # Perfect week should have high score
    assert health["score"] >= 80


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
