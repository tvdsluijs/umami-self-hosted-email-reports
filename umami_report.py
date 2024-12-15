import os
from helpers.config import load_config
from helpers.auth import authenticate
from helpers.report import generate_html_email
from helpers.email import send_email
from helpers.umami import get_umami_data
from helpers.scheduler import schedule_reports, should_send_report
from helpers.files import load_last_sent, save_last_sent
from helpers.date_ranges import calculate_date_range

# Load configurations
CONFIG = load_config("config.json")
WEBSITES = load_config("websites_config.json")

COMPANY = CONFIG["company"]
UMAMI_API_URL = CONFIG["umami"]["api_url"]
UMAMI_USERNAME = CONFIG["umami"]["username"]
UMAMI_PASSWORD = CONFIG["umami"]["password"]
SMTP_CONFIG = CONFIG["smtp"]

BEARER_TOKEN = None

def process_website(site, now):
    frequency = site["frequency"]
    website_id = site["website_id"]
    website_name = site["name"]
    recipients = site["emails"]
    what_stats = site["what_stats"]

    LOGS_DIR = "logs"
    os.makedirs(LOGS_DIR, exist_ok=True)
    last_sent_file = os.path.join(LOGS_DIR, f"last_sent_{website_id}.json")

    last_sent = load_last_sent(last_sent_file)

    if should_send_report(last_sent, frequency):
        range_start, range_end = calculate_date_range(now, frequency)
        stats = get_umami_data(UMAMI_API_URL, BEARER_TOKEN, website_id, range_start, range_end, frequency, what_stats)
        # report = generate_report(website_name, stats, pages, referrers)
        report = generate_html_email(COMPANY, frequency, stats, what_stats, website_name)
        subject = f"{frequency.capitalize()}ly Website Report for {website_name}"
        send_email(subject, report, recipients, SMTP_CONFIG)
        save_last_sent(last_sent_file, now)

if __name__ == "__main__":
    BEARER_TOKEN = authenticate(UMAMI_API_URL, UMAMI_USERNAME, UMAMI_PASSWORD)
    schedule_reports(WEBSITES, process_website)
