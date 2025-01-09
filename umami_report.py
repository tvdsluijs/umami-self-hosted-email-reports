"""
📊 Umami Self-Hosted Email Reports Script

This script generates and sends analytics reports for websites managed by
Umami Analytics. It supports various frequencies, including daily, weekly,
monthly, quarterly, and yearly reports.

Features:
- Fetch analytics data from Umami's API.
- Generate reports as HTML emails.
- Schedule and send reports via email to multiple recipients.

Modules Used:
- `helpers.config`: Load configuration files.
- `helpers.auth`: Authenticate with the Umami API.
- `helpers.report`: Generate HTML email reports.
- `helpers.email`: Send emails via SMTP.
- `helpers.umami`: Fetch analytics data from the Umami API.
- `helpers.scheduler`: Schedule and process reports.
- `helpers.date_ranges`: Calculate date ranges for the reports.

Author: Theo van der Sluijs
Contact: [📧 Email](mailto:theo@vandersluijs.nl)
License: MIT
"""
import os
import json
from sys import exit
# Import helper functions and modules
from helpers.config import load_config
from helpers.auth import authenticate
from helpers.frequency_options import frequency_options
from helpers.report import generate_html_email
from helpers.email import send_email
from helpers.umami import get_umami_data
from helpers.scheduler import schedule_reports, should_send_report
from helpers.date_ranges import calculate_date_range

# Load configurations
CONFIG = load_config("config.json")  # General configurations, e.g., SMTP and Umami credentials
WEBSITES = load_config("websites_config.json")  # Website-specific configurations like frequency and emails

COMPANY = CONFIG["company"]  # Company details for branding in email
UMAMI_API_URL = CONFIG["umami"]["api_url"]  # Base URL for Umami API
UMAMI_USERNAME = CONFIG["umami"]["username"]  # Umami API username
UMAMI_PASSWORD = CONFIG["umami"]["password"]  # Umami API password
SMTP_CONFIG = CONFIG["smtp"]  # SMTP configuration for sending emails

BEARER_TOKEN = None  # Global variable for storing the Umami API authentication token

# Vertalingen laden
def load_translation(lang_code):
    with open(f"{lang_code}.json", 'r') as f:
        return json.load(f)

def process_website(site, now):
    """
    Process a single website to determine if a report should be sent,
    fetch data, generate the report, and send it via email.

    Args:
        site (dict): The website configuration dictionary.
        now (datetime): The current date and time.
    """
    # Extract website-specific configuration
    lang = site.get('lang', 'en')  # Language code for translations
    frequency = site.get('frequency', 'daily')  # Frequency of the report (default: daily)
    send_day = site.get('send_day', [])  # Days to send the report (e.g., ["mon", "fri"])

    website_id = site["website_id"]  # Unique identifier for the website in Umami
    website_name = site["name"]  # Display name for the website
    recipients = site["emails"]  # List of email recipients

    if not website_id or not website_name or not recipients:
        print("Website ID, name, and email recipients must be provided, there is a problem with your websites_config.json.")
        exit(1)

    what_stats = site.get("what_stats", ["stats", "events", "urls", "referrers", "browsers", "oses", "devices", "countries"])  # List of metrics to include in the report
    top = site.get('top', 5) # show the number of statistics per chapter, default 5

    # get the correct laguage
    translations = load_translation(lang)
    # add frequency_options to the translation of the frequency (options)
    translations['frequency_options'] = frequency_options(frequency, translations)

    # Check if the report should be sent based on frequency and send_day
    if should_send_report(frequency, send_day):
        # Calculate the date range for the report based on frequency
        range_start, range_end = calculate_date_range(now, frequency)

        # Fetch analytics data from the Umami API
        stats = get_umami_data(UMAMI_API_URL, BEARER_TOKEN, website_id, range_start, range_end, frequency, what_stats)

        # Get the current directory of the script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_file = "style.css"
        # Combine the current directory with the CSS file name
        css_file_path = os.path.join(current_dir, css_file)

        # Generate the HTML email report
        report = generate_html_email(COMPANY, frequency, stats, what_stats, css_file_path, website_name, top, translations)

        # Compose the subject line for the email
        subject = f"{frequency.capitalize()}ly Website Report for {website_name}"

        # Send the report via email
        send_email(subject, report, recipients, SMTP_CONFIG)

if __name__ == "__main__":
    """
    Main script execution:
    - Authenticate with the Umami API.
    - Schedule reports for all websites in the configuration.
    """
    # Authenticate with the Umami API and retrieve a bearer token
    BEARER_TOKEN = authenticate(UMAMI_API_URL, UMAMI_USERNAME, UMAMI_PASSWORD)

    # Schedule and process reports for all websites
    schedule_reports(WEBSITES, process_website)
