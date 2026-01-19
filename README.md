<div align="center">

# 🎯 Alpha-X

### Time Tracking & Personal Optimization System

**A smart personal tracking system that analyzes your daily activities and sends weekly insights to WhatsApp**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=flat&logo=whatsapp&logoColor=white)](https://www.twilio.com/docs/whatsapp)

</div>

---

## Features

- 📊 Automatically fetches data from Google Forms responses
- 🎯 Tracks your 4 main goals: Career, Health, Marriage, Investments
- 🔧 **Flexible tracking** - works even if you remove columns (skip goals you don't track)
- 📱 Sends weekly insights via WhatsApp
- 🤖 Intelligent analysis and recommendations
- ⏰ Automated weekly reports every Sunday
- 📈 Detailed monthly summaries with trend analysis

## Goals Priority

1. **Career Growth** - Coding time, focus, and performance
2. **Health & Fitness** - Protein intake, workouts, sleep, sunshine
3. **Marriage** - Relationship goals tracking
4. **Investments** - (To be tracked)

**💡 Note**: All goals are optional! The system automatically adapts to whatever you track. Remove any columns from your form and the reports still work. See [CUSTOMIZATION.md](CUSTOMIZATION.md) for details.

## Setup

### Prerequisites

- Python 3.9+
- Google Cloud account with Sheets API enabled
- Twilio account for WhatsApp messaging

### Installation

```bash
# Clone the repository
cd Alpha-X

# Install dependencies
pip install -r requirements.txt
```

### Configuration

#### 1. Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create credentials (Service Account):
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the details and create
   - Click on the created service account
   - Go to "Keys" tab > "Add Key" > "Create new key" > JSON
5. Download the JSON key file
6. Save as `credentials/google_sheets_credentials.json`
7. **Important**: Share your Google Sheet with the service account email (found in the JSON file under `client_email`)

#### 2. Twilio WhatsApp Setup

1. Sign up at [Twilio](https://www.twilio.com/)
2. For development/testing:
   - Use Twilio Sandbox for WhatsApp
   - Send "join <your-sandbox-code>" to +1 415 523 8886 from your WhatsApp
3. For production:
   - Apply for a WhatsApp Business API account
   - Get a WhatsApp-enabled phone number
4. Note your Account SID and Auth Token from the Twilio Console

#### 3. Environment Variables

Create a `.env` file in the root directory:

```env
# Google Sheets Configuration
GOOGLE_FORM_URL=your_google_form_url
GOOGLE_SHEET_URL=your_google_sheet_responses_file


# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+your_country_code_and_number
```

## Usage

### Quick Summary (Recommended)

**Weekly Summary** - Get summary of your last 7 entries:
```bash
python src/summarize_last_week.py
```
This automatically fetches the last 7 rows from your sheet, analyzes them, and sends insights to WhatsApp.

**Monthly Summary** - Get detailed analysis of last 30 days:
```bash
python src/summarize_last_month.py
```
Provides comprehensive monthly report with trends, week-over-week comparisons, and detailed insights.

### Manual Run

Generate and send weekly insights:
```bash
python src/main.py
```

Generate insights for specific week:
```bash
python src/main.py --weeks-ago 1  # Last week's data
```

### Automated Weekly Reports

Run the scheduler (sends reports every Sunday at 1 PM):
```bash
python src/scheduler.py
```

**Want to set up automatic weekly summaries?** See [SCHEDULING_GUIDE.md](docs/SCHEDULING_GUIDE.md) for:
- Cron jobs (Mac/Linux)
- Task Scheduler (Windows)
- GitHub Actions (Cloud-based)
- Docker containers

### Test Connection

Test your setup:
```bash
python src/test_connection.py
```

## Project Structure

```
Alpha-X/
├── src/
│   ├── main.py                  # Main application entry
│   ├── summarize_last_week.py   # Quick 7-day summary (recommended)
│   ├── summarize_last_month.py  # Detailed 30-day analysis
│   ├── sheets_client.py         # Google Sheets integration
│   ├── analyzer.py              # Data analysis and insights
│   ├── whatsapp_client.py       # WhatsApp messaging
│   ├── scheduler.py             # Weekly report scheduler
│   └── config.py                # Configuration management
├── credentials/
│   └── google_sheets_credentials.json  # Google API credentials (not in git)
├── tests/
│   └── test_analyzer.py     # Unit tests
├── requirements.txt
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment variables
├── .gitignore
└── README.md
```

## How It Works

1. **Data Collection**: Fetches your daily form responses from Google Sheets
2. **Analysis**: Analyzes your performance across all 4 goals
3. **Insights Generation**: Creates personalized insights with strengths and improvement areas
4. **Delivery**: Sends formatted report to your WhatsApp

## Sample Weekly Report

```
📊 Weekly Report (Jan 5-11, 2026)

🎯 CAREER GROWTH (Priority #1)
✅ Coded 5/7 days - Good!
⚠️ Focus: 3 days razor sharp, 4 days multi-tasking
💡 Tip: Try Pomodoro technique for better focus

💪 HEALTH & FITNESS (Priority #2)
✅ Protein: 6/7 days >= 100g - Excellent!
✅ Workout: 5/7 days - Great consistency!
⚠️ Sleep: Avg 6.5 hrs (Need 7-8 hrs)
✅ Sunshine: 6/7 days
💡 Tip: Sleep earlier for better recovery

❤️ MARRIAGE (Priority #3)
⚠️ Average performance this week
💡 Tip: Schedule quality time together

📈 OVERALL PERFORMANCE
Week Trend: Better than last week! 🎉
Happy Days: 5/7 days
Keep pushing forward! 💪

🌟 This Week's Win:
Great job on protein and workout consistency!

⚠️ Focus Area for Next Week:
Improve sleep quality and career focus
```

## Development

### Run Tests

```bash
pytest tests/
```

### Lint Code

```bash
flake8 src/
black src/
```

## Customization

Want to track only certain goals? No problem!

- **Remove columns** from your Google Form - the system adapts automatically
- **Add custom goals** - see [CUSTOMIZATION.md](CUSTOMIZATION.md)
- **Rename sections** - update the config to match your needs
- The system **never crashes** due to missing columns

## Troubleshooting

### Google Sheets Access Denied

- Make sure you've shared the spreadsheet with the service account email
- Check that the Google Sheets API is enabled in your project

### WhatsApp Messages Not Sending

- Verify your Twilio credentials are correct
- If using sandbox, ensure you've joined the sandbox with your WhatsApp number
- Check your Twilio account balance (free account still works)

### No Data Found

- Verify the GOOGLE_SHEET_URL is correct
- Check that your sheet has data in the expected format
- Ensure the sheet name/tab is correct in the code

### "Not tracking X data" Messages

- This is normal if you removed columns from your form
- The system skips sections with no data automatically
- To start tracking, add the questions back to your form

## License

MIT License

## Author

**Prabhat Gupta** - Senior AI Engineer | LLM Systems Builder

<p align="left">
  <a href="https://www.linkedin.com/in/prabhatkgupta-kgp168/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://github.com/prabhatkgupta" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
  <a href="https://prabhat-gupta-tech.netlify.app/" target="_blank">
    <img src="https://img.shields.io/badge/Website-FF7139?style=for-the-badge&logo=firefox&logoColor=white" alt="Website">
  </a>
  <a href="mailto:prabhat16aug@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
  </a>
</p>

---

**💡 Built with ❤️ for personal growth and productivity tracking**

