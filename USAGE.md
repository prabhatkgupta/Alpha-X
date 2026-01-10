# Alpha-X Usage Guide

Quick reference for running Alpha-X commands.

## 🚀 Most Common Use Case

### Get Summary of Last 7 Entries

```bash
python src/summarize_last_week.py
```

**What it does:**
- Automatically fetches the **last 7 rows** from your Google Sheet
- No date filtering - just grabs your most recent entries
- Analyzes performance across all 4 goals
- Sends insights to your WhatsApp

**When to use:**
- Daily check-ins
- Anytime you want to see how your last week went
- When you've filled 7+ entries in your form

---

## 📊 Other Commands

### 1. Weekly Report (Date-Based)

```bash
# Current week (Monday to Sunday)
python src/main.py

# Last week
python src/main.py --weeks-ago 1

# Preview without sending
python src/main.py --dry-run
```

**What it does:**
- Filters data by calendar week (Monday-Sunday)
- Useful for weekly reviews
- More precise date filtering

---

### 2. Test Your Setup

```bash
python src/test_connection.py
```

**What it does:**
- Validates configuration
- Tests Google Sheets connection
- Tests WhatsApp messaging
- Runs end-to-end flow

---

### 3. Automated Scheduler

```bash
python src/scheduler.py
```

**What it does:**
- Runs continuously in background
- Sends report every Sunday at 8 PM
- Uses date-based weekly filtering

---

## 🤔 Which Command Should I Use?

### Use `summarize_last_week.py` if:
- ✅ You want quick insights on demand
- ✅ You fill your form daily but not exactly 7 days per week
- ✅ You want the most recent data regardless of dates
- ✅ You prefer simplicity

### Use `main.py` if:
- ✅ You want calendar week-based reports (Mon-Sun)
- ✅ You need historical weekly data (weeks-ago parameter)
- ✅ You want dry-run preview mode
- ✅ You want precise date filtering

### Use `scheduler.py` if:
- ✅ You want automatic weekly reports
- ✅ You don't want to run commands manually
- ✅ You prefer set-it-and-forget-it automation

---

## 📝 Examples

### Scenario 1: Daily Check-In
```bash
# You filled the form for last 7 days, want to see progress
python src/summarize_last_week.py
```

### Scenario 2: Weekly Review on Sunday
```bash
# Automated - runs every Sunday at 8 PM
python src/scheduler.py
```

### Scenario 3: Look Back at Previous Week
```bash
# Get insights from 2 weeks ago
python src/main.py --weeks-ago 2
```

### Scenario 4: First Time Setup
```bash
# Test everything works
python src/test_connection.py

# Generate your first summary
python src/summarize_last_week.py
```

---

## 💡 Pro Tips

1. **For best results**: Fill your daily form consistently
2. **Quick insights**: Use `summarize_last_week.py` whenever you want
3. **Automation**: Set up `scheduler.py` to run in background
4. **Historical analysis**: Use `main.py --weeks-ago N` to look back

---

## 🆘 Troubleshooting

### No data found?
- Make sure you've filled at least 1 entry in your Google Form
- Check that GOOGLE_SHEET_ID is correct in `.env`
- Verify you've shared the sheet with service account

### WhatsApp not working?
- Check Twilio credentials in `.env`
- For testing: Join Twilio Sandbox (see SETUP_GUIDE.md)
- Verify your WhatsApp number format: `whatsapp:+countrycode_number`

### Script errors?
```bash
# Activate virtual environment first
source venv/bin/activate

# Then run your command
python src/summarize_last_week.py
```

---

**Happy tracking! 🎯**

