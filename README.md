# cve_fetcher
This repository contains Python scripts for fetching and maintaining a database of CVEs (Common Vulnerabilities and Exposures). The scripts are designed to fetch new CVEs, filter them based on relevant tools and hardware, send notifications to a Discord webhook, and perform regular maintenance on the database to keep it up to date.
## Files in this Repository

- `fetch_cves.py`: Script to fetch CVEs from the NVD API and send notifications to Discord.
- `db_maintenance.py`: Script to remove old CVE entries from the database.
- `tools.txt`: A list of tools and hardware to filter relevant CVEs.
- `cves_db.json`: The database file storing CVE entries.
- `myenv`: Python virtual environment directory (not included in the repository).
- `requierments.txt`: Requierments for python-pip (dependencies).
- `requierments.txt`: Requierments for python-pip (Flask app) (dependencies).
- `Dockerfile`: To build and deploy the app in a container.
- `entrypoint.sh`: For the deployment of the container
- `cve_web_app`: Sub-directory containing files for Flask App.

## Getting Started

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

### Setting Up

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/cve_fetcher.git
    cd cve_fetcher
    ```

2. **Create a virtual environment (optional but recommended):**
    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. **Install required packages:**
    ```sh
    pip install requests tinydb
    ```

4. **Set up your NVD API Key:**
    - Obtain your API key from the [NVD API Key Request Page](https://nvd.nist.gov/developers/request-an-api-key).
    - Replace the placeholder `NVD_API_KEY` in `fetch_cves.py` with your actual API key.

5. **Set up your Discord Webhook URL:**
    - Follow this [guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) to create a Discord webhook.
    - Replace the placeholder `WEBHOOK_URL` in `fetch_cves.py` with your actual webhook URL.

6. **(Optional) Set up other webhooks:**
    - **Slack:** Follow [this guide](https://api.slack.com/messaging/webhooks) to create a Slack webhook.
    - **Microsoft Teams:** Follow [this guide](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) to create a Teams webhook.
    - **Mattermost:** Follow [this guide](https://docs.mattermost.com/developer/webhooks-incoming.html) to create a Mattermost webhook.

### Script Descriptions

#### `fetch_cves.py`

This script fetches CVEs from the NVD API based on the tools and hardware specified in `tools.txt`. It performs the following steps:
1. Fetches the latest CVEs from the NVD API.
2. Filters the CVEs based on the tools and hardware listed in `tools.txt`.
3. Saves the new CVEs to `cves_db.json` to avoid duplicates.
4. Sends the filtered CVEs to a specified Discord webhook.

The script ensures that only new CVEs are fetched by checking the database for existing entries. This prevents re-fetching of CVEs that have already been processed.

#### `db_maintenance.py`

This script performs maintenance on the `cves_db.json` database. It:
1. Removes CVE entries older than a specified number of days (default is 14 days).
2. Keeps the database file size manageable by removing outdated entries.
3. Ensures that the fetch script only fetches new CVEs without re-fetching old ones by maintaining the most recent entries.

### Running the Scripts

1. **Fetch CVEs:**
    ```sh
    python fetch_cves.py
    ```

2. **Database Maintenance:**
    ```sh
    python db_maintenance.py
    ```

### Automating with Cron Jobs

To automate the execution of these scripts, you can set up cron jobs.

1. **Open the crontab editor:**
    ```sh
    crontab -e
    ```

2. **Add the following lines to schedule the scripts:**

    ```sh
    # Run fetch_cves.py every day at 2 AM
    0 2 * * * /path/to/your/env/bin/python /path/to/your/repo/fetch_cves.py

    # Run db_maintenance.py every Sunday at 3 AM
    0 3 * * 0 /path/to/your/env/bin/python /path/to/your/repo/db_maintenance.py
    ```

    Replace `/path/to/your/env` with the actual path to your Python virtual environment, and `/path/to/your/repo` with the path to your cloned repository.

### Testing

You can manually run the scripts to test if they are working correctly:

```sh
python fetch_cves.py
python db_maintenance.py

### Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

### License

This project is licensed under the MIT License.


This `README.md` file provides an overview of the repository, detailed instructions for setting up and running the scripts, descriptions of each script, and information on how to automate the process using cron jobs.
