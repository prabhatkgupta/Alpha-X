#!/bin/bash

# Setup script for Alpha-X scheduler

echo "🚀 Alpha-X Scheduler Setup"
echo "=" * 50
echo ""

# Create logs directory
mkdir -p logs
echo "✅ Created logs directory"

# Create .github/workflows directory for GitHub Actions
mkdir -p .github/workflows
echo "✅ Created .github/workflows directory"

# Create GitHub Actions workflow
cat > .github/workflows/weekly-summary.yml << 'EOF'
name: Weekly Summary Report

on:
  schedule:
    # Runs every Sunday at 1 PM UTC (adjust timezone as needed)
    - cron: '0 13 * * 0'
  workflow_dispatch:  # Allows manual trigger from GitHub UI

jobs:
  send-summary:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Create credentials file
        env:
          GOOGLE_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
        run: |
          mkdir -p credentials
          echo "$GOOGLE_CREDENTIALS" > credentials/google_sheets_credentials.json
      
      - name: Run weekly summary
        env:
          GOOGLE_SHEET_ID: ${{ secrets.GOOGLE_SHEET_ID }}
          GOOGLE_SHEET_URL: ${{ secrets.GOOGLE_SHEET_URL }}
          GOOGLE_FORM_URL: ${{ secrets.GOOGLE_FORM_URL }}
          TWILIO_ACCOUNT_SID: ${{ secrets.TWILIO_ACCOUNT_SID }}
          TWILIO_AUTH_TOKEN: ${{ secrets.TWILIO_AUTH_TOKEN }}
          TWILIO_WHATSAPP_FROM: ${{ secrets.TWILIO_WHATSAPP_FROM }}
          YOUR_WHATSAPP_NUMBER: ${{ secrets.YOUR_WHATSAPP_NUMBER }}
        run: |
          python src/summarize_last_week.py
EOF

echo "✅ Created GitHub Actions workflow"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1️⃣ For Local Scheduling (Cron):"
echo "   Run: crontab -e"
echo "   Add: 0 13 * * 0 cd $(pwd) && $(pwd)/venv/bin/python src/summarize_last_week.py >> logs/cron.log 2>&1"
echo ""
echo "2️⃣ For Python Scheduler:"
echo "   Run: python src/scheduler.py"
echo ""
echo "3️⃣ For GitHub Actions (Cloud):"
echo "   - Commit and push .github/workflows/weekly-summary.yml"
echo "   - Add secrets in GitHub repo settings"
echo "   - See docs/SCHEDULING_GUIDE.md for details"
echo ""
echo "📚 For detailed instructions, see: docs/SCHEDULING_GUIDE.md"
echo ""

