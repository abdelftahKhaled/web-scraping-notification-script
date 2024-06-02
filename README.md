# Web Scraping Notification Script

## Overview

This script is designed to monitor specific websites and notify users whenever a new article is published. It identifies newly posted articles, extracts relevant information such as publication dates, and sends notifications to keep users updated with the latest content.

## Features

- **Website Monitoring**: Continuously monitors specified websites for new content.
- **Real-time Notifications**: Sends instant notifications to users when a new article is detected.
- **Content Extraction**: Extracts key information from new articles, including publication date and title.
- **User Alerts**: Alerts users with details about the newly published articles, including the source website and the publication date.

## Installation

To install and run this script, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/web-scraping-notification-script.git
    ```
2. Navigate to the project directory:
    ```sh
    cd web-scraping-notification-script
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Configure the list of websites to monitor in the `config.py` file.
2. Run the script:
    ```sh
    python main.py
    ```
3. The script will start monitoring the specified websites and send notifications when new articles are published.


