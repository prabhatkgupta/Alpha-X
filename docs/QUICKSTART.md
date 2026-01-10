# Quick Start Guide

Get up and running in 10 minutes!

## ⚡ Fast Setup

### 1. Install Dependencies (2 mins)

```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

### 2. Set Up Google Sheets (3 mins)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google Sheets API
3. Create Service Account → Download JSON key
4. Save as `credentials/google_sheets_credentials.json`
5. Share your Google Sheet (containing form responses) with service account email

### 3. Set Up Twilio WhatsApp (3 mins)

1. Sign up at [Twilio](https://www.twilio.com/)
2. Go to WhatsApp Sandbox in console
3. Send "join <code>" from your WhatsApp to sandbox number
4. Copy Account SID and Auth Token

### 4. Configure .env (1 min)

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 5. Test & Run (1 min)

```bash
# Test everything
python src/test_connection.py

# Quick summary of last 7 entries (recommended)
python src/summarize_last_week.py

# Or generate weekly report with date filtering
python src/main.py --dry-run
python src/main.py
```

## 🎯 Done!

You should receive a weekly report on WhatsApp!

## 📅 Automate (Optional)

```bash
# Run scheduler (sends every Sunday at 8 PM)
python src/scheduler.py
```

## 🆘 Need Help?

See [SETUP_GUIDE.md](../SETUP_GUIDE.md) for detailed instructions.

## 📊 Sample Report

```
📊 Weekly Report (Jan 5-11, 2026)

🎯 CAREER GROWTH (Priority #1)
✅ Coded 5/7 days - Good!
⚠️ Focus: 3 days razor sharp, 4 days multi-tasking
💡 Tip: Try Pomodoro technique

💪 HEALTH & FITNESS (Priority #2)
✅ Protein: 6/7 days >= 100g - Excellent!
✅ Workout: 5/7 days - Great!
⚠️ Sleep: Avg 6.5 hrs (Need 7-8 hrs)

❤️ MARRIAGE (Priority #3)
⚠️ Average performance this week
💡 Tip: Schedule quality time

📈 OVERALL PERFORMANCE
Week Trend: Better than last week! 🎉
Happy Days: 5/7 days

👍 Good week! Room for improvement 💪
```

