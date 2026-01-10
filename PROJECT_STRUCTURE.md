# Project Structure

Complete overview of Alpha-X - Your personal tracking and insights system.

## 📁 Directory Structure

```
Alpha-X/
│
├── 📄 README.md                    # Main project documentation
├── 📄 QUICKSTART.md                # Quick setup guide (10 mins)
├── 📄 SETUP_GUIDE.md               # Detailed setup instructions
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📄 LICENSE                      # MIT License
├── 📄 requirements.txt             # Python dependencies
├── 📄 pytest.ini                   # Test configuration
├── 📄 .env.example                 # Environment variables template
├── 📄 .env                         # Your secrets (not in git)
├── 📄 .gitignore                   # Git ignore rules
├── 📜 setup.sh                     # Automated setup script
│
├── 📂 src/                         # Source code
│   ├── __init__.py                 # Package initializer
│   ├── config.py                   # Configuration management
│   ├── sheets_client.py            # Google Sheets integration
│   ├── analyzer.py                 # Data analysis & insights
│   ├── whatsapp_client.py          # WhatsApp messaging via Twilio
│   ├── summarize_last_week.py      # Quick 7-day summary (recommended)
│   ├── summarize_last_month.py     # Detailed 30-day monthly analysis
│   ├── main.py                     # Main application entry
│   ├── scheduler.py                # Automated weekly reports
│   └── test_connection.py          # Connection test suite
│
├── 📂 credentials/                 # API credentials (not in git)
│   ├── README.md                   # Setup instructions
│   └── google_sheets_credentials.json  # Google API key
│
├── 📂 tests/                       # Test suite
│   ├── __init__.py
│   └── test_analyzer.py            # Analyzer unit tests
│
└── 📂 venv/                        # Virtual environment (not in git)
```

## 🔧 Core Components

### 1. **config.py** - Configuration Manager
- Loads environment variables
- Validates setup
- Manages API credentials
- Defines goal priorities

### 2. **sheets_client.py** - Google Sheets Client
- Connects to Google Sheets API
- Fetches form responses
- Filters data by week/date range
- Provides data as pandas DataFrames

### 3. **analyzer.py** - Intelligence Engine
- Analyzes performance across 4 goals:
  - Career Growth (coding, focus, performance)
  - Health & Fitness (protein, workout, sleep, sunshine)
  - Marriage (relationship quality)
  - Investments (future enhancement)
- Generates insights and recommendations
- Calculates performance scores
- Identifies focus areas

### 4. **whatsapp_client.py** - WhatsApp Messenger
- Connects to Twilio API
- Sends formatted reports
- Handles message length limits
- Provides test functionality

### 5. **summarize_last_week.py** - Quick Summary (Recommended)
- Fetches last 7 rows from Google Sheet
- No date filtering - just grabs most recent entries
- Analyzes and sends to WhatsApp
- Perfect for daily/on-demand summaries

### 6. **main.py** - Application Entry Point
- Orchestrates the full workflow
- Fetches data → Analyzes → Sends report
- Command-line interface
- Supports dry-run mode

### 7. **scheduler.py** - Automation Scheduler
- Runs continuously
- Triggers weekly reports (Sunday 8 PM)
- Can be customized for different schedules

### 8. **test_connection.py** - Setup Validator
- Tests configuration
- Validates Google Sheets connection
- Tests WhatsApp messaging
- End-to-end flow verification

## 📊 Data Flow

```
Google Form (You fill daily)
      ↓
Google Sheets (Stores responses)
      ↓
sheets_client.py (Fetches data)
      ↓
analyzer.py (Analyzes & generates insights)
      ↓
whatsapp_client.py (Formats & sends)
      ↓
WhatsApp (You receive weekly insights)
```

## 🎯 Your Goals Tracking

### Priority #1: Career Growth
- **Metrics**: Coding days, focus quality, goal achievement
- **Target**: 85%+ coding days, razor-sharp focus
- **Insights**: Consistency tracking, focus recommendations

### Priority #2: Health & Fitness
- **Metrics**: Protein intake, workouts, sleep hours, sunshine
- **Target**: 100g protein, 5+ workouts/week, 7-8 hrs sleep
- **Insights**: Health patterns, recovery recommendations

### Priority #3: Marriage
- **Metrics**: Relationship quality (Good/Okayish/Not good)
- **Target**: 70%+ good days
- **Insights**: Quality time suggestions

### Priority #4: Investments
- **Status**: Coming soon!

## 🚀 Usage Examples

### Quick Summary of Last 7 Entries (Recommended)
```bash
python src/summarize_last_week.py
```

### Generate Current Week Report
```bash
python src/main.py
```

### Generate Last Week Report
```bash
python src/main.py --weeks-ago 1
```

### Preview Without Sending
```bash
python src/main.py --dry-run
```

### Run Automated Scheduler
```bash
python src/scheduler.py
```

### Test Your Setup
```bash
python src/test_connection.py
```

### Run Unit Tests
```bash
pytest tests/
```

## 🔐 Security

### Files NOT in Git (Protected):
- `.env` - Your secrets
- `credentials/` - API keys
- `venv/` - Virtual environment
- `__pycache__/` - Python cache

### Files in Git:
- Source code
- Documentation
- Tests
- `.env.example` (template only)

## 📈 Future Enhancements

Potential features to add:
- [ ] Investment tracking integration
- [ ] Monthly/yearly summaries
- [ ] Trend graphs and visualizations
- [ ] Goal setting and progress tracking
- [ ] AI-powered personalized recommendations
- [ ] Mobile app integration
- [ ] Multiple notification channels (Email, Telegram)
- [ ] Habit streak tracking
- [ ] Comparative analytics (vs previous weeks/months)

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Data Processing**: pandas, numpy
- **Google Sheets**: gspread, google-auth
- **WhatsApp**: Twilio
- **Scheduling**: schedule
- **Testing**: pytest
- **Configuration**: python-dotenv

## 📚 Documentation Files

1. **README.md** - Main project overview
2. **QUICKSTART.md** - Get started in 10 minutes
3. **SETUP_GUIDE.md** - Step-by-step detailed setup
4. **PROJECT_STRUCTURE.md** - This file (architecture overview)
5. **credentials/README.md** - Credentials setup guide

## 🎓 Learning Resources

If you want to extend this project:

- [gspread Documentation](https://docs.gspread.org/)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [schedule Documentation](https://schedule.readthedocs.io/)

## 🤝 Contributing

This is your personal project, but if you want to:
- Add new features
- Improve insights
- Fix bugs
- Enhance documentation

Feel free to modify and improve!

## 📞 Support

For issues or questions:
1. Check documentation files
2. Run `python src/test_connection.py`
3. Review error messages carefully
4. Verify credentials in `.env`

---

**Built with ❤️ for personal growth tracking**

