"""Data analyzer for generating insights from daily tracking data."""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
from collections import Counter


class PersonalizationAnalyzer:
    """Analyzer for personal tracking data."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize analyzer with data."""
        self.df = df
        self.total_days = len(df)
    
    def analyze_career(self) -> Dict[str, Any]:
        """Analyze career growth metrics (Priority #1)."""
        analysis = {
            'priority': 1,
            'title': '🎯 CAREER GROWTH',
            'metrics': {},
            'insights': [],
            'score': 0,  # 0-100
            'has_data': False
        }
        
        if self.df.empty:
            return analysis
        
        # Coding days
        if 'coding' in self.df.columns:
            analysis['has_data'] = True
            coding_yes = (self.df['coding'] == 'Yes').sum()
            coding_rate = coding_yes / self.total_days if self.total_days > 0 else 0
            analysis['metrics']['coding_days'] = f"{coding_yes}/{self.total_days} days"
            
            if coding_rate >= 0.85:
                analysis['insights'].append(f"✅ Coded {coding_yes}/{self.total_days} days - Excellent!")
                analysis['score'] += 35
            elif coding_rate >= 0.7:
                analysis['insights'].append(f"✅ Coded {coding_yes}/{self.total_days} days - Good!")
                analysis['score'] += 25
            else:
                analysis['insights'].append(f"⚠️ Only coded {coding_yes}/{self.total_days} days - Need more consistency")
                analysis['score'] += 10
        
        # Focus quality
        if 'focus' in self.df.columns:
            analysis['has_data'] = True
            focus_counts = self.df['focus'].value_counts()
            sharp_days = focus_counts.get('Good, razor sharp', 0)
            multitask_days = focus_counts.get("I was multi-tasking, not good focus", 0)
            
            analysis['metrics']['focus'] = f"{sharp_days} days sharp, {multitask_days} days multi-tasking"
            
            if sharp_days >= multitask_days:
                analysis['insights'].append(f"✅ Focus: {sharp_days} days razor sharp - Great!")
                analysis['score'] += 35
            else:
                analysis['insights'].append(f"⚠️ Focus: {multitask_days} days multi-tasking - Need improvement")
                analysis['insights'].append("💡 Tip: Try Pomodoro technique (25 min focus + 5 min break)")
                analysis['score'] += 15
        
        # Career focus
        if 'career_focus' in self.df.columns:
            analysis['has_data'] = True
            career_counts = self.df['career_focus'].value_counts()
            good_days = career_counts.get('Good, achieved my today\'s goal', 0)
            lazy_days = career_counts.get('Lazy, didn\'t wanted to work', 0)
            
            if good_days >= 5:
                analysis['insights'].append(f"✅ Achieved daily goals {good_days} days - Fantastic!")
                analysis['score'] += 30
            elif lazy_days >= 3:
                analysis['insights'].append(f"⚠️ {lazy_days} lazy days - Let's fix this!")
                analysis['insights'].append("💡 Tip: Break goals into smaller tasks")
                analysis['score'] += 10
        
        # If no career data at all
        if not analysis['has_data']:
            analysis['insights'].append("ℹ️ No career tracking data found in your sheet")
        
        return analysis
    
    def analyze_health(self) -> Dict[str, Any]:
        """Analyze health & fitness metrics (Priority #2)."""
        analysis = {
            'priority': 2,
            'title': '💪 HEALTH & FITNESS',
            'metrics': {},
            'insights': [],
            'score': 0,
            'has_data': False
        }
        
        if self.df.empty:
            return analysis
        
        # Protein intake
        if 'protein' in self.df.columns:
            analysis['has_data'] = True
            protein_met = (self.df['protein'] == '>= 100g').sum()
            protein_rate = protein_met / self.total_days if self.total_days > 0 else 0
            analysis['metrics']['protein'] = f"{protein_met}/{self.total_days} days"
            
            if protein_rate >= 0.85:
                analysis['insights'].append(f"✅ Protein: {protein_met}/{self.total_days} days >= 100g - Excellent!")
                analysis['score'] += 25
            elif protein_rate >= 0.6:
                analysis['insights'].append(f"✅ Protein: {protein_met}/{self.total_days} days >= 100g - Good!")
                analysis['score'] += 15
            else:
                analysis['insights'].append(f"⚠️ Protein: Only {protein_met}/{self.total_days} days >= 100g")
                analysis['insights'].append("💡 Tip: Prep protein-rich meals in advance")
                analysis['score'] += 5
        
        # Workout
        if 'workout' in self.df.columns:
            analysis['has_data'] = True
            workout_days = (self.df['workout'] == 'Yes').sum()
            workout_rate = workout_days / self.total_days if self.total_days > 0 else 0
            analysis['metrics']['workout'] = f"{workout_days}/{self.total_days} days"
            
            if workout_rate >= 0.7:
                analysis['insights'].append(f"✅ Workout: {workout_days}/{self.total_days} days - Great consistency!")
                analysis['score'] += 25
            elif workout_rate >= 0.5:
                analysis['insights'].append(f"⚠️ Workout: {workout_days}/{self.total_days} days - Could be better")
                analysis['score'] += 15
            else:
                analysis['insights'].append(f"⚠️ Workout: Only {workout_days}/{self.total_days} days")
                analysis['insights'].append("💡 Tip: Start with 20-min daily workouts")
                analysis['score'] += 5
        
        # Sleep analysis
        if 'sleep' in self.df.columns:
            analysis['has_data'] = True
            # Extract numeric hours from sleep strings
            sleep_hours = []
            for val in self.df['sleep']:
                if isinstance(val, str):
                    if 'hrs' in val or 'hr' in val:
                        # Extract first number from string like "7 hrs" or ">=10 hrs"
                        import re
                        match = re.search(r'(\d+)', val)
                        if match:
                            sleep_hours.append(int(match.group(1)))
            
            if sleep_hours:
                avg_sleep = sum(sleep_hours) / len(sleep_hours)
                analysis['metrics']['avg_sleep'] = f"{avg_sleep:.1f} hrs"
                
                if avg_sleep >= 7 and avg_sleep <= 9:
                    analysis['insights'].append(f"✅ Sleep: Avg {avg_sleep:.1f} hrs - Perfect!")
                    analysis['score'] += 25
                elif avg_sleep >= 6:
                    analysis['insights'].append(f"⚠️ Sleep: Avg {avg_sleep:.1f} hrs (Target: 7-8 hrs)")
                    analysis['insights'].append("💡 Tip: Sleep earlier for better recovery")
                    analysis['score'] += 15
                else:
                    analysis['insights'].append(f"⚠️ Sleep: Avg {avg_sleep:.1f} hrs - Too low!")
                    analysis['insights'].append("💡 Tip: Prioritize sleep - it affects everything")
                    analysis['score'] += 5
        
        # Sunshine
        if 'sunshine' in self.df.columns:
            analysis['has_data'] = True
            sunshine_days = (self.df['sunshine'] == 'Yes').sum()
            if sunshine_days >= 5:
                analysis['insights'].append(f"✅ Sunshine: {sunshine_days}/{self.total_days} days - Good!")
                analysis['score'] += 25
            else:
                analysis['insights'].append(f"⚠️ Sunshine: {sunshine_days}/{self.total_days} days")
                analysis['insights'].append("💡 Tip: Morning sun boosts vitamin D & mood")
        
        # If no health data at all
        if not analysis['has_data']:
            analysis['insights'].append("ℹ️ No health/fitness tracking data found in your sheet")
        
        return analysis
    
    def analyze_marriage(self) -> Dict[str, Any]:
        """Analyze marriage goals (Priority #3)."""
        analysis = {
            'priority': 3,
            'title': '❤️ MARRIAGE',
            'metrics': {},
            'insights': [],
            'score': 0,
            'has_data': False
        }
        
        if self.df.empty or 'marriage' not in self.df.columns:
            analysis['insights'].append("ℹ️ Not tracking marriage/relationship data")
            return analysis
        
        analysis['has_data'] = True
        
        marriage_counts = self.df['marriage'].value_counts()
        good_days = marriage_counts.get('Good', 0)
        okayish_days = marriage_counts.get('Okayish', 0)
        not_good_days = marriage_counts.get('Not good', 0)
        
        analysis['metrics']['status'] = f"Good: {good_days}, Okayish: {okayish_days}, Not good: {not_good_days}"
        
        good_rate = good_days / self.total_days if self.total_days > 0 else 0
        
        if good_rate >= 0.7:
            analysis['insights'].append(f"✅ Strong relationship focus: {good_days}/{self.total_days} good days")
            analysis['score'] = 100
        elif good_rate >= 0.4:
            analysis['insights'].append(f"⚠️ Moderate performance: {good_days} good, {okayish_days} okayish days")
            analysis['insights'].append("💡 Tip: Schedule quality time together")
            analysis['score'] = 60
        else:
            analysis['insights'].append(f"⚠️ Needs attention: {not_good_days} not good days")
            analysis['insights'].append("💡 Tip: Have an open conversation about expectations")
            analysis['score'] = 30
        
        return analysis
    
    def analyze_overall_performance(self) -> Dict[str, Any]:
        """Analyze overall performance and happiness."""
        analysis = {
            'title': '📈 OVERALL PERFORMANCE',
            'metrics': {},
            'insights': []
        }
        
        if self.df.empty:
            return analysis
        
        # Performance trend
        if 'performance' in self.df.columns:
            perf_counts = self.df['performance'].value_counts()
            better = perf_counts.get('Yes, better than yesterday', 0)
            same = perf_counts.get('Same as yesterday', 0)
            worse = perf_counts.get('Worst than yesterday', 0)
            
            if better >= worse:
                analysis['insights'].append(f"Week Trend: Better than yesterday on {better}/{self.total_days} days 🎉")
            else:
                analysis['insights'].append(f"Week Trend: {worse} worse days - Let's turn this around")
        
        # Happiness
        if 'happiness' in self.df.columns:
            happy_counts = self.df['happiness'].value_counts()
            happy = happy_counts.get('Yes, I am happy', 0)
            neutral = happy_counts.get('Slightly Neutral, could do better', 0)
            bad = happy_counts.get('No, I performed bad', 0)
            
            analysis['metrics']['happy_days'] = f"{happy}/{self.total_days} days"
            
            if happy >= 5:
                analysis['insights'].append(f"Happy Days: {happy}/{self.total_days} days - Great! 😊")
            elif happy >= 3:
                analysis['insights'].append(f"Happy Days: {happy}/{self.total_days} days - Keep going! 💪")
            else:
                analysis['insights'].append(f"Happy Days: Only {happy}/{self.total_days} days")
                analysis['insights'].append("💡 Remember: Progress > Perfection")
        
        # Day overview
        if 'day_overview' in self.df.columns:
            overview_counts = self.df['day_overview'].value_counts()
            hard_enjoyed = overview_counts.get('Did hard work - enjoyed', 0)
            procrastinated = overview_counts.get('Procrastinated', 0)
            
            if hard_enjoyed >= 4:
                analysis['insights'].append(f"🌟 This Week's Win: Did hard work & enjoyed it {hard_enjoyed} days!")
            if procrastinated >= 3:
                analysis['insights'].append(f"⚠️ Procrastinated {procrastinated} days - Break tasks smaller")
        
        return analysis
    
    def generate_weekly_report(self) -> str:
        """Generate complete weekly report."""
        if self.df.empty:
            return "❌ No data available for this week"
        
        # Get date range
        start_date = self.df['timestamp'].min()
        end_date = self.df['timestamp'].max()
        
        report_lines = [
            f"📊 Weekly Report ({start_date.strftime('%b %d')}-{end_date.strftime('%b %d, %Y')})",
            ""
        ]
        
        # Analyze each goal area
        career = self.analyze_career()
        health = self.analyze_health()
        marriage = self.analyze_marriage()
        overall = self.analyze_overall_performance()
        
        # Build report - only include sections with data
        tracked_goals = []
        for section in [career, health, marriage]:
            if section.get('has_data', False) or section['insights']:
                tracked_goals.append(section['title'])
                report_lines.append(section['title'])
                for insight in section['insights']:
                    report_lines.append(insight)
                report_lines.append("")
        
        # Overall section
        report_lines.append(overall['title'])
        for insight in overall['insights']:
            report_lines.append(insight)
        report_lines.append("")
        
        # Calculate overall score (only from tracked areas)
        tracked_sections = [s for s in [career, health, marriage] if s.get('has_data', False)]
        if tracked_sections:
            total_score = sum(s['score'] for s in tracked_sections) / len(tracked_sections)
            
            if total_score >= 70:
                report_lines.append("🎉 Excellent week overall! Keep it up! 💪")
            elif total_score >= 50:
                report_lines.append("👍 Good week! Room for improvement 💪")
            else:
                report_lines.append("⚠️ Tough week. Focus on one thing at a time 💪")
        
        # Add tracking summary
        if tracked_goals:
            report_lines.append("")
            report_lines.append(f"📋 Currently tracking: {len(tracked_goals)} goal(s)")
        
        return "\n".join(report_lines)
    
    def get_focus_areas(self) -> List[str]:
        """Identify top 3 focus areas for next week."""
        focus_areas = []
        
        # Check each metric
        career = self.analyze_career()
        health = self.analyze_health()
        marriage = self.analyze_marriage()
        
        # Prioritize based on scores
        if career['score'] < 60:
            focus_areas.append("Career: Improve coding consistency and focus")
        if health['score'] < 60:
            focus_areas.append("Health: Better sleep and workout routine")
        if marriage['score'] < 60:
            focus_areas.append("Marriage: More quality time together")
        
        return focus_areas[:3]  # Top 3


if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        'timestamp': pd.date_range('2026-01-05', periods=7),
        'coding': ['Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'No'],
        'focus': ['Good, razor sharp'] * 4 + ["I was multi-tasking, not good focus"] * 3,
        'protein': ['>= 100g'] * 6 + ['< 100g'],
        'workout': ['Yes'] * 5 + ['No'] * 2,
        'sleep': ['7 hrs', '6 hrs', '7 hrs', '8 hrs', '6 hrs', '7 hrs', '6 hrs'],
        'marriage': ['Good', 'Okayish', 'Good', 'Okayish', 'Good', 'Good', 'Okayish'],
        'happiness': ['Yes, I am happy'] * 5 + ['Slightly Neutral, could do better'] * 2
    }
    
    df = pd.DataFrame(sample_data)
    analyzer = PersonalizationAnalyzer(df)
    
    print(analyzer.generate_weekly_report())

