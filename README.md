# CVE Fetcher and Dashboard

This repository contains Python scripts for fetching and maintaining a database of CVEs (Common Vulnerabilities and Exposures), along with a Flask web application to display the CVEs. The scripts are designed to fetch new CVEs, filter them based on relevant tools and hardware, send notifications to a Discord webhook, and perform regular maintenance on the database to keep it up to date.

## Project Structure

```
cve_fetch/
├── crontab
├── cve_web_app/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── index.html
│   │   │   └── visualizations.html
│   │   └── static/
│   │       └── style.css
│   ├── cves_db.json
│   ├── requirements.txt
│   ├── run.py
│   └── venv/
├── cves_db.json
├── db_maintenance.py
├── docker_commands.txt
├── Dockerfile
├── entrypoint.sh
├── fetch_cves.py
├── fetch_env/
├── manage_envs.sh
├── myenv/
├── README.md
├── requirements.txt
└── tools.txt

```

## Files in this Repository

- `fetch_cves.py`: Script to fetch CVEs from the NVD API and send notifications to Discord.
- `db_maintenance.py`: Script to remove old CVE entries from the database.
- `tools.txt`: A list of tools and hardware to filter relevant CVEs.
- `cves_db.json`: The database file storing CVE entries.
- `Dockerfile`: Dockerfile to build the Docker image.
- `entrypoint.sh`: Entry point script to start cron jobs and the Flask application.
- `cve_web_app/`: Directory containing the Flask web application.

## Getting Started

### Prerequisites

- Docker
- Docker Compose (optional but recommended)
- Python 3.x (if running without Docker)
- Virtual environment (optional but recommended)

### Setting Up

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/cve_fetcher.git
    cd cve_fetcher
    ```

2. **Create and configure the `.env` file:**
    ```sh
    cp .env.example .env
    ```
    Fill in the `.env` file with your NVD API key and Discord webhook URL.

    ```env
    NVD_API_KEY=your_nvd_api_key
    DISCORD_WEBHOOK_URL=your_discord_webhook_url
    ```

### Using Docker

1. **Build the Docker image:**
    ```sh
    docker build -t cve_fetch_app .
    ```

2. **Run the Docker container:**
    ```sh
    docker run -d -p 5000:5000 cve_fetch_app
    ```

3. **Access the Flask web application:**
    Open your browser and go to `http://localhost:5000`.

### Using Python Environment (Alternative to Docker)

1. **Create a virtual environment (optional but recommended):**
    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

2. **Install required packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up your NVD API Key and Discord Webhook URL in the `.env` file.**

4. **Run the Flask web application:**
    ```sh
    python cve_web_app/run.py
    ```

5. **Access the Flask web application:**
    Open your browser and go to `http://localhost:5000`.

## Script Descriptions

### `fetch_cves.py`

This script fetches CVEs from the NVD API based on the tools and hardware specified in `tools.txt`. It performs the following steps:
1. Fetches the latest CVEs from the NVD API.
2. Filters the CVEs based on the tools and hardware listed in `tools.txt`.
3. Saves the new CVEs to `cves_db.json` to avoid duplicates.
4. Sends the filtered CVEs to a specified Discord webhook.

### `db_maintenance.py`

This script performs maintenance on the `cves_db.json` database. It:
1. Removes CVE entries older than a specified number of days (default is 14 days).
2. Keeps the database file size manageable by removing outdated entries.
3. Ensures that the fetch script only fetches new CVEs without re-fetching old ones by maintaining the most recent entries.

## Automating with Cron Jobs

The cron jobs are set up automatically within the Docker container to run the scripts periodically.

- `fetch_cves.py`: Runs every 15 minutes.
- `db_maintenance.py`: Runs every Sunday at 11 AM.

### Monitoring and Logs

You can monitor the logs to ensure the cron jobs are running correctly:

1. **Access the running container:**
    ```sh
    docker exec -it <container_id> /bin/bash
    ```

2. **Check the logs:**
    ```sh
    cat /var/log/cron_fetch_cves.log
    cat /var/log/cron_db_maintenance.log
    ```

### Webhooks for Other Platforms

**Slack**:
- Follow [this guide](https://api.slack.com/messaging/webhooks) to create a Slack webhook.
- Replace the Discord webhook URL with your Slack webhook URL in the `.env` file.

**Microsoft Teams**:
- Follow [this guide](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) to create a Teams webhook.
- Replace the Discord webhook URL with your Teams webhook URL in the `.env` file.

**Mattermost**:
- Follow [this guide](https://docs.mattermost.com/developer/webhooks-incoming.html) to create a Mattermost webhook.
- Replace the Discord webhook URL with your Mattermost webhook URL in the `.env` file.

### Testing

You can manually run the scripts to test if they are working correctly:

```sh
python fetch_cves.py
python db_maintenance.py
```

### Running the Flask App

The Flask app is included in the Docker container and will be accessible at `http://localhost:5000` once the container is running.

### License

This project is licensed under the MIT License.

### Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

This `README.md` file provides an overview of the repository, detailed instructions for setting up and running the Docker container, descriptions of each script, and information on how to automate the process using cron jobs within the Docker container. Additionally, it includes instructions for setting up webhooks for other apps such as Slack or Microsoft Teams.
