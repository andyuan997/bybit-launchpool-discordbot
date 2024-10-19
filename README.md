# Bybit Launchpool Scraper and Discord Notifier

This Python script is designed to scrape the latest Bybit Launchpool announcements and send a notification to a specified Discord channel when new announcements are found. The script periodically checks for updates and notifies via Discord if new listings are detected.

## Features

- **Web Scraping**: Uses `requests` and `BeautifulSoup` to scrape Bybit Launchpool announcements across multiple pages.
- **Discord Notification**: Sends new announcements to a Discord channel via a webhook.
- **Scheduled Checks**: Continuously monitors for new announcements with a set time interval.

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `BeautifulSoup`
  - `json`
  - `time`

You can install the required libraries using the following command:

```bash
pip install requests beautifulsoup4
