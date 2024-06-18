#!/bin/bash

# Start cron service
service cron start

# Add cron job for fetch_cves.py
(crontab -l ; echo "*/15 * * * * cd /app && /usr/local/bin/python /app/fetch_cves.py >> /var/log/cron_fetch_cves.log 2>&1") | crontab -

# Add cron job for db_maintenance.py
(crontab -l ; echo "0 11 * * 0 cd /app && /usr/local/bin/python /app/db_maintenance.py >> /var/log/cron_db_maintenance.log 2>&1") | crontab -

# Run the Flask app
/usr/local/bin/python /app/cve_web_app/run.py

# Keep the container running
tail -f /dev/null
