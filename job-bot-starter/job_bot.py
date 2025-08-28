import requests
import pandas as pd
import time
import os

# Headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Number of retries if server error occurs
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def fetch_remotive_jobs():
    url = "https://remotive.io/api/remote-jobs"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("jobs", [])
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Skipping fetch.")
                return []

def save_jobs_to_csv(jobs):
    if not jobs:
        print("No jobs fetched.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(jobs)
    
    # Create output folder if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Save with a timestamped filename
    filename = f"output/jobs_{int(time.time())}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}")

def main():
    print("Fetching jobs...")
    jobs = fetch_remotive_jobs()
    save_jobs_to_csv(jobs)
    print("Done!")

if __name__ == "__main__":
    main()
