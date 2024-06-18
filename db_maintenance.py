import datetime
from tinydb import TinyDB, Query

# Configuration
DB_FILE = 'cves_db.json'
RETENTION_DAYS = 14

def main():
    db = TinyDB(DB_FILE)
    CVE = Query()

    # Calculate the cutoff date for retention
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=RETENTION_DAYS)

    def is_older(entry):
        try:
            entry_date_str = entry['data']['cve']['published']
            entry_date = datetime.datetime.fromisoformat(entry_date_str.replace("Z", "+00:00"))

            # Ensure both dates are timezone-aware for comparison
            if entry_date.tzinfo is none:
                entry_date = entry_date.replace(tzinfo=datetime.timezone.utc)
            
            return entry_date < cutoff_date
        except KeyError as e:
            print(f"Error processing entry {entry}: {e}")
            return False

    # Collect IDs of entries to remove
    all_entries = db.all()
    to_remove = [entry.doc_id for entry in all_entries if is_older(entry)]

    # Ensure we keep the most recent entry if there are any entries to remove
    if to_remove and len(to_remove) < len(all_entries):
        most_recent_entry = max(all_entries, key=lambda entry: entry['data']['cve']['published'])
        if most_recent_entry.doc_id in to_remove:
            to_remove.remove(most_recent_entry.doc_id)

    # Remove the old entries
    db.remove(doc_ids=to_remove)
    print(f"Removed {len(to_remove)} CVEs older than {RETENTION_DAYS} days.")

if __name__ == "__main__":
    main()
