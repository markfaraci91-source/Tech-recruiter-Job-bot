import os
from pathlib import Path
from datetime import datetime, timezone
import requests
import pandas as pd

REMOTIVE_URL = "https://remotive.io/api/remote-jobs"

# Adjust these to your taste
KEYWORDS = [
    "recruiter",
    "recruiting",
    "talent acquisition",
    "technical recruiter",
    "tech recruiter",
    "sourcer",
    "technical sourcer",
]
EXCLUDE_TERMS = [
    # add strings that should exclude a listing, e.g. "non-tech", "campus"
]

OUTPUT_DIR = Path("data")
OUTPUT_CSV = OUTPUT_DIR / "latest.csv"


def fetch_remotive_jobs():
    # Pull all remote jobs once, then filter locally
    r = requests.get(REMOTIVE_URL, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("jobs", [])


def is_match(title: str, description: str) -> bool:
    t = (title or "").lower()
    d = (description or "").lower()
    if not any(k in t for k in KEYWORDS):
        return False
    if any(x.lower() in t or x.lower() in d for x in EXCLUDE_TERMS):
        return False
    return True


def normalize(job):
    # Map Remotive fields to a compact schema
    pub_date = job.get("publication_date")
    try:
        # Example format: "2024-09-05T16:45:43"
        dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
    except Exception:
        dt = None

    return {
        "Date": dt.isoformat().replace("+00:00", "Z") if dt else pub_date,
        "Title": job.get("title"),
        "Company": job.get("company_name"),
        "Location": job.get("candidate_required_location"),
        "Job Type": job.get("job_type"),
        "Category": job.get("category"),
        "Salary": job.get("salary"),
        "URL": job.get("url"),
        "Source": "Remotive",
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    jobs = fetch_remotive_jobs()

    matches = []
    for j in jobs:
        title = j.get("title", "")
        desc = j.get("description", "")
        if is_match(title, desc):
            matches.append(normalize(j))

    if not matches:
        print("No matching jobs found.")
        # still write an empty CSV with headers for consistency
        pd.DataFrame(columns=[
            "Date","Title","Company","Location","Job Type","Category","Salary","URL","Source"
        ]).to_csv(OUTPUT_CSV, index=False)
        return

    df = pd.DataFrame(matches).drop_duplicates(subset=["URL"])

    # Sort newest first by Date (ISO8601 strings work lexicographically when consistent)
    df = df.sort_values(by="Date", ascending=False)

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote {len(df)} jobs to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
