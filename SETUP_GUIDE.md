# Detailed Setup Guide

Complete step-by-step guide to set up Alpha-X.

## Prerequisites

- Python 3.9 or higher
- Google account (for accessing your Google Form responses)
- Twilio account (free tier works for testing)

## Step 1: Install Python Dependencies

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Google Sheets API Setup

### 2.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown (top left)
3. Click "New Project"
4. Name it "Alpha-X" and click "Create"

### 2.2 Enable Google Sheets API

1. In your project, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"

### 2.3 Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in:
   - Service account name: `alpha-x`
   - Service account ID: (auto-generated)
   - Click "Create and Continue"
4. Skip the optional steps, click "Done"

### 2.4 Download Credentials

1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Click "Create" - a file will download
6. Save this file as `credentials/google_sheets_credentials.json`

### 2.5 Share Your Google Sheet

1. Open your JSON credentials file
2. Find the `client_email` field (looks like: `alpha-x@your-project.iam.gserviceaccount.com`)
3. Open your Google Sheet (the one containing your form responses)
4. Click "Share" button (top right)
5. Add the service account email
6. Give it "Viewer" access
7. Click "Send"

## Step 3: Twilio WhatsApp Setup

### 3.1 Create Twilio Account

1. Go to [Twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. Verify your email and phone number

### 3.2 Get Credentials

1. Go to Twilio Console Dashboard
2. Note your:
   - Account SID
   - Auth Token

### 3.3 Set Up WhatsApp Sandbox (For Testing)

1. In Twilio Console, go to "Messaging" > "Try it out" > "Send a WhatsApp message"
2. You'll see a sandbox number and a code like `join abc-def`
3. From your WhatsApp, send that message to the sandbox number
4. You should receive a confirmation message

**Note**: The sandbox is free but has limitations. For production, you'll need to apply for WhatsApp Business API.

## Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:
```env
# Your Google Sheet ID (from the URL)
GOOGLE_SHEET_ID=your_google_sheet_id_here
   
   # Twilio credentials (from Twilio Console)
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   
   # Twilio sandbox number for WhatsApp (found in Twilio Console)
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   
   # Your WhatsApp number (must include country code)
   YOUR_WHATSAPP_NUMBER=whatsapp:+your_country_code_and_number
   ```

## Step 5: Test Your Setup

Run the test script to verify everything is working:

```bash
python src/test_connection.py
```

This will test:
- ✅ Configuration validation
- ✅ Google Sheets connection
- ✅ WhatsApp messaging
- ✅ End-to-end flow

## Step 6: Run Manual Report

Generate and send a weekly report:

```bash
# For current week
python src/main.py

# For last week
python src/main.py --weeks-ago 1

# Dry run (don't send, just print)
python src/main.py --dry-run
```

## Step 7: Set Up Automated Reports

### Option A: Keep Script Running

```bash
python src/scheduler.py
```

This will run continuously and send reports every Sunday at 8 PM.

### Option B: Use System Cron (Linux/Mac)

1. Edit crontab:
   ```bash
   crontab -e
   ```

2. Add this line (adjust path):
   ```cron
   0 20 * * 0 cd /path/to/Alpha-X && /path/to/venv/bin/python src/main.py
   ```

This runs every Sunday at 8 PM.

### Option C: Use Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Weekly, Sunday, 8:00 PM
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `src/main.py`
7. Start in: `C:\path\to\Alpha-X`

## Troubleshooting

### Google Sheets "Permission Denied"

- Make sure you shared the sheet with the service account email
- Check that the GOOGLE_SHEET_ID in .env is correct
- Verify Google Sheets API is enabled in your project

### WhatsApp Messages Not Sending

- Verify Twilio credentials are correct
- For sandbox: Make sure you joined the sandbox from your WhatsApp
- Check Twilio account balance (free trial has $15 credit)
- Verify WhatsApp number format includes country code

### "No module named 'config'"

- Make sure you're in the src/ directory or running from root with `python src/main.py`
- Activate your virtual environment: `source venv/bin/activate`

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Support

If you run into issues:

1. Check the error messages carefully
2. Review this guide step-by-step
3. Test each component individually using `test_connection.py`
4. Make sure all credentials are correct in `.env`

## Next Steps

Once everything is working:

1. Run `python src/main.py --dry-run` to see a sample report
2. Test with `python src/main.py` to send your first report
3. Set up the scheduler for automated weekly reports
4. Enjoy your personalized insights! 🎉

