import requests
import json
import datetime
import os
import re
import time
from tinydb import TinyDB, Query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
NVD_API_KEY = os.getenv('NVD_API_KEY')
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
BASE_API_URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
TOOLS_FILE = 'tools.txt'
DB_FILE = 'cves_db.json'
FETCH_INTERVAL = 3600 * 24  # 24 hours
BATCH_SIZE = 5  # Number of CVEs per batch
SLEEP_TIME = 2  # Time to sleep between batches

# Load tools and hardware from file
def load_tools(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Fetch CVEs from NVD API
def fetch_cves():
    headers = {
        'apiKey': NVD_API_KEY
    }
    pub_end_date = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    pub_start_date = pub_end_date - datetime.timedelta(seconds=FETCH_INTERVAL)
    
    params = {
        'resultsPerPage': 100,
        'startIndex': 0,
        'pubStartDate': pub_start_date.isoformat().replace('+00:00', 'Z'),
        'pubEndDate': pub_end_date.isoformat().replace('+00:00', 'Z')
    }
    response = requests.get(BASE_API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Filter CVEs based on tools and hardware
def filter_cves(cves, tools):
    filtered_cves = []
    for cve in cves.get('vulnerabilities', []):
        cve_json = json.dumps(cve).lower()
        for tool in tools:
            if re.search(re.escape(tool.lower()), cve_json):
                filtered_cves.append(cve)
                break
    return filtered_cves

# Save new CVEs to the database and avoid duplicates
def save_cves(cves):
    db = TinyDB(DB_FILE)
    CVE = Query()
    new_cves = []
    for cve in cves:
        if not db.contains(CVE.id == cve['cve']['id']):
            db.insert({'id': cve['cve']['id'], 'data': cve})
            new_cves.append(cve)
    return new_cves

# Send CVEs to Discord webhook in batches
def send_to_discord(cves):
    # Sort CVEs by severity
    def get_severity(cve):
        try:
            return cve['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']
        except (KeyError, IndexError):
            return 0

    cves_sorted = sorted(cves, key=get_severity, reverse=True)
    
    total_batches = (len(cves_sorted) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(total_batches):
        batch = cves_sorted[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
        batch_content = ""
        for cve in batch:
            cve_id = cve['cve']['id']
            cve_description = cve['cve']['descriptions'][0]['value']
            cve_url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            references = [ref['url'] for ref in cve['cve'].get('references', [])]

            try:
                cve_severity = cve['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseSeverity']
            except (KeyError, IndexError):
                cve_severity = 'UNKNOWN'
            
            batch_content += f"**New CVE Found: [{cve_id}]({cve_url})**\n"
            batch_content += f"Severity: {cve_severity}\n"
            batch_content += f"Description: {cve_description}\n"
            batch_content += "References:\n"
            for ref in references:
                batch_content += f"{ref}\n"
            batch_content += "\n"

        if len(batch_content) > 2000:  # Discord message limit is 2000 characters
            batch_content = batch_content[:1997] + '...'
        
        data = {
            "content": batch_content
        }
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 5))
            print(f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print(f"Batch {i + 1} of {total_batches} sent successfully.")
        if i < total_batches - 1:
            print(f"Sent batch {i + 1}, continuing to next batch after sleeping for rate limit...")
            time.sleep(SLEEP_TIME)

# Main function
def main():
    tools = load_tools(TOOLS_FILE)
    print(f"Loaded tools: {tools}")
    
    try:
        cves = fetch_cves()
        print("Fetched CVEs from NVD API.")
        
        filtered_cves = filter_cves(cves, tools)
        print(f"Filtered CVEs: {len(filtered_cves)} found.")
        
        new_cves = save_cves(filtered_cves)
        print(f"New CVEs: {len(new_cves)} to be sent to Discord.")
        
        if new_cves:
            send_to_discord(new_cves)
            print("Sent new CVEs to Discord.")
        else:
            print("No new CVEs to send.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
