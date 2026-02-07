# Scheduling Guide - Automated Weekly & Monthly Reports

This guide explains how to run **weekly** (every Sunday) and **monthly** (1st of each month) summaries automatically.

## 📅 What Gets Scheduled

| Script | When | Action |
|--------|------|--------|
| `summarize_last_week.py` | **Every Sunday** (e.g. 1:00 PM) | Last 7 days from sheet → WhatsApp |
| `summarize_last_month.py` | **1st of every month** (e.g. 2:00 PM) | Last 30 days summary → WhatsApp |

---

## 🎯 Where to Deploy (Recommended Options)

| Option | Best for | Weekly | Monthly | Cost |
|--------|----------|--------|---------|------|
| **GitHub Actions** | Cloud, no machine needed | ✅ | ✅ | Free (public repos) |
| **Cron (Mac/Linux)** | Your own computer always on | ✅ | ✅ | Free |
| **Windows Task Scheduler** | Windows PC always on | ✅ | ✅ | Free |
| **Render Cron** | Managed cloud cron | ✅ | ✅ | Free tier available |
| **Railway / Fly.io** | Cron + optional app | ✅ | ✅ | Free tier |

**Recommendation:** Use **GitHub Actions** so reports run even when your laptop is off. Workflows are already in `.github/workflows/` (see Method 4 below).

---

## 🚀 Method 1: Python Scheduler (Recommended for Personal Use)

The built-in `scheduler.py` uses Python's `schedule` library.

### Run in Foreground (Testing)

```bash
cd /Users/prabhatgupta/Downloads/repos/Alpha-X
source venv/bin/activate
python src/scheduler.py
```

**Note**: This keeps the terminal open. Press `Ctrl+C` to stop.

### Run in Background (Mac/Linux)

```bash
cd /Users/prabhatgupta/Downloads/repos/Alpha-X
source venv/bin/activate
nohup python src/scheduler.py > logs/scheduler.log 2>&1 &
```

This runs in the background and logs to `logs/scheduler.log`.

### Stop Background Process

```bash
# Find the process
ps aux | grep scheduler.py

# Kill it (replace PID with actual process ID)
kill <PID>
```

---

## ⚙️ Method 2: System Cron Job (Mac/Linux)

Cron is built into Unix systems and runs even after reboot.

### Step 1: Make Sure Script Works

```bash
cd /Users/prabhatgupta/Downloads/repos/Alpha-X
source venv/bin/activate
python src/summarize_last_week.py
```

### Step 2: Create Cron Job

```bash
# Open crontab editor
crontab -e
```

### Step 3: Add These Lines

```cron
# Weekly: every Sunday at 1 PM
0 13 * * 0 cd /path/to/Alpha-X && /path/to/Alpha-X/venv/bin/python src/summarize_last_week.py >> logs/cron.log 2>&1

# Monthly: 1st of every month at 2 PM
0 14 1 * * cd /path/to/Alpha-X && /path/to/Alpha-X/venv/bin/python src/summarize_last_month.py >> logs/cron_monthly.log 2>&1
```

Replace `/path/to/Alpha-X` and `/path/to/Alpha-X/venv` with your actual project and venv paths.

### Step 4: Save and Verify

```bash
# List your cron jobs
crontab -l
```

### Cron Time Format

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, 0 and 7 are Sunday)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

### Examples

```cron
# Every Sunday at 1 PM
0 13 * * 0 <command>

# Every day at 9 AM
0 9 * * * <command>

# Every Monday at 8 PM
0 20 * * 1 <command>
```

---

## 🪟 Method 3: Windows Task Scheduler

### Step 1: Open Task Scheduler

1. Press `Win + R`
2. Type `taskschd.msc` and press Enter

### Step 2: Create Basic Task

1. Click **"Create Basic Task"** in the right panel
2. Name: `Alpha-X Weekly Summary`
3. Description: `Send weekly insights every Sunday at 1 PM`

### Step 3: Set Trigger

1. Trigger: **Weekly**
2. Start date: Today
3. Days: **Sunday**
4. Time: **1:00 PM**

### Step 4: Set Action

1. Action: **Start a program**
2. Program: `C:\path\to\Alpha-X\venv\Scripts\python.exe`
3. Arguments: `src\summarize_last_week.py`
4. Start in: `C:\path\to\Alpha-X`

### Step 5: Finish and Test

1. Click **Finish**
2. Right-click the task → **Run** to test

---

## ☁️ Method 4: GitHub Actions (Cloud-Based) — Recommended

Runs in the cloud; no need to keep your computer on. Two workflows are included:

- **`.github/workflows/weekly-summary.yml`** — every Sunday at 1:00 PM UTC  
- **`.github/workflows/monthly-summary.yml`** — 1st of every month at 2:00 PM UTC  

You can change the time in each file (e.g. `cron: '0 13 * * 0'` = minute 0, hour 13 = 1 PM UTC). Both support **Run workflow** from the Actions tab for manual runs.

### Step 1: Workflows Already Created

No need to create files; they are in the repo. After cloning/pushing, go to the **Actions** tab to see "Weekly Summary (Sunday)" and "Monthly Summary (1st of Month)".

### Step 2: Add Secrets to GitHub

1. Go to your repo: `https://github.com/prabhatkgupta/Alpha-X`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:
   - `GOOGLE_SHEET_ID`: Your sheet ID
   - `TWILIO_ACCOUNT_SID`: Your Twilio SID
   - `TWILIO_AUTH_TOKEN`: Your Twilio token
   - `TWILIO_WHATSAPP_FROM`: `whatsapp:+14155238886`
   - `YOUR_WHATSAPP_NUMBER`: `whatsapp:+918789653411`
   - `GOOGLE_CREDENTIALS`: Paste entire JSON content from your credentials file

### Step 3: Enable Actions

1. Go to **Actions** tab in your repo
2. Enable workflows if prompted

### Benefits of GitHub Actions

- ✅ Runs in the cloud (no local machine needed)
- ✅ Free for public repos (2000 minutes/month)
- ✅ Runs even if your computer is off
- ✅ Easy to monitor via GitHub UI

---

## 🐳 Method 5: Docker Container (Advanced)

Run as a Docker container for isolation.

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/scheduler.py"]
```

### Build and Run

```bash
docker build -t alpha-x-scheduler .
docker run -d --name alpha-x \
  --env-file .env \
  -v $(pwd)/credentials:/app/credentials \
  alpha-x-scheduler
```

---

## 📊 Monitoring & Logs

### View Logs (Python Scheduler)

```bash
tail -f logs/scheduler.log
```

### View Logs (Cron)

```bash
tail -f logs/cron.log
```

### View Logs (GitHub Actions)

Go to **Actions** tab → Click on workflow run → View logs

---

## 🆘 Troubleshooting

### Script Not Running

```bash
# Check if process is running
ps aux | grep scheduler

# Check cron logs
tail -f /var/log/syslog | grep CRON
```

### Environment Variables Not Loading

Make sure `.env` file is in the correct location and the script can access it:

```bash
cd /Users/prabhatgupta/Downloads/repos/Alpha-X
cat .env  # Verify it exists
```

### Permissions Issues (Cron)

```bash
# Make sure scripts are executable
chmod +x src/scheduler.py
chmod +x src/summarize_last_week.py
```

### Time Zone Issues

Python `schedule` and cron use system time. Check your timezone:

```bash
# Mac/Linux
date
timedatectl  # Linux only

# If time is wrong, adjust your system timezone
```

---

## 🎯 Recommended Setup

**For automated runs without keeping your PC on:**
- Use **Method 4 (GitHub Actions)** — weekly and monthly workflows run in the cloud for free.

**For personal use (Mac/Linux always on):**
- Use **Method 2 (Cron)** — add both weekly and monthly cron lines above.

**For testing:**
- Use **Method 1 (Python Scheduler)** or run scripts manually before enabling cron/GitHub Actions.

---

## ✅ Verification

After setting up, verify it works:

```bash
# Manual test
python src/summarize_last_week.py

# Check you receive WhatsApp message
# If successful, your scheduler will work the same way
```

---

**💡 Need help?** Check the main [README.md](../README.md) or [SETUP_GUIDE.md](../SETUP_GUIDE.md)

