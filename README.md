# Freelance Job Notifier

This project is a Python-based automated script designed to periodically check for new job listings on the Ukrainian freelance site freelance.ua. The script compares the job IDs with a local database to identify new listings. When a new job is detected, it sends a notification to a specified Telegram channel with the job title and link. The script operates only between 8 AM and 12 AM.

### Features
*    Automated Job Checking: Periodically checks for new job listings.
 *   Local Database Comparison: Uses a local database to keep track of processed job IDs.
 *   Telegram Notifications: Sends notifications to a Telegram channel with the job title and link.
 *   Scheduled Operation: Runs daily from 8 AM to 12 AM.
### Prerequisites
 *   Python 3.x
 *   requests library for HTTP requests
 *   beautifulsoup4 for parsing HTML
 *   tinydb for local database management
 *   python-telegram-bot library for sending Telegram notifications

### Usage
To ensure the script ran 24/7 on a Linux server and to easily view the logs, tmux was used. tmux is a terminal multiplexer that allows the creation and management of multiple terminal sessions from a single window.
