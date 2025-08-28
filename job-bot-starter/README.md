# Remote Technical Recruiter Job Bot

A tiny Python bot that fetches fresh remote **technical recruiter** roles (via the free Remotive API) and stores them in `data/latest.csv`. A GitHub Action runs it on a schedule and commits updated results back to the repo.

## What it does
- Pulls remote job listings from Remotive
- Filters for roles with *recruit* in the title (Recruiter, Recruiting, Talent Acquisition)
- Saves `data/latest.csv` sorted by newest first
- GitHub Actions runs twice per day and commits changes automatically

## Run locally
```bash
# 1) (optional) create and activate a virtualenv
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# 2) install dependencies
pip install -r requirements.txt

# 3) run the bot
python job_bot.py

# output: data/latest.csv
```

## Customizing the search
Open `job_bot.py` and edit the `KEYWORDS` or `EXCLUDE_TERMS` lists to broaden or narrow results. By default it searches for generic recruiter titles and skips obvious non-matches.

## How to use with GitHub Actions
1. Create a **new public repo** on GitHub.
2. Upload all files from this starter (or drag-and-drop the ZIP contents).
3. Go to the **Actions** tab – enable workflows for this repo if prompted.
4. The workflow runs on push and on a schedule. See the latest run logs in **Actions** and your CSV at `data/latest.csv`.

> Note: GitHub Actions uses UTC for `cron`. This workflow runs every 12 hours by default.
