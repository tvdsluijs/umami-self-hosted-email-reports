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
- `helpers.general`: Has some general functions
- `helpers.email`: Send emails via SMTP.
- `helpers.umami`: Fetch analytics data from the Umami API.
- `helpers.scheduler`: Schedule and process reports.
- `helpers.date_ranges`: Calculate date ranges for the reports.

Author: Theo van der Sluijs
Contact: [📧 Email](mailto:theo@vandersluijs.nl)
License: MIT
"""
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import os
import re
import logging
from logging.handlers import TimedRotatingFileHandler
from sys import exit
import traceback

from jinja2 import Environment, FileSystemLoader, TemplateError
from weasyprint import HTML

# Import helper functions and modules
from helpers.config import load_config
from helpers.auth import authenticate
from helpers.frequency_options import frequency_options
from helpers.general import capitalize_sentences, check_create_dir, type_mapping
from helpers.email import send_email
from helpers.umami import get_umami_data
from helpers.translation_validator import load_smart_translation
from helpers.scheduler import schedule_reports, should_send_report
from helpers.date_ranges import calculate_date_range

# Load configurations
CONFIG: Dict[str, Any] = load_config("configs/config.json")
WEBSITES: List[Dict[str, Any]] = load_config("configs/websites_config.json")

COMPANY: Dict[str, str] = CONFIG["company"]
UMAMI_API_URL: str = CONFIG["umami"]["api_url"]
UMAMI_USERNAME: str = CONFIG["umami"]["username"]
UMAMI_PASSWORD: str = CONFIG["umami"]["password"]
SMTP_CONFIG: Dict[str, Any] = CONFIG["smtp"]

BEARER_TOKEN: Optional[str] = None

def setup_logging() -> None:
    """Configure logging with rotation and formatting."""
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_handler = TimedRotatingFileHandler(
        'logs/umami_report.log',
        when='midnight',
        interval=1,
        backupCount=7
    )
    log_handler.suffix = "%Y-%m-%d"
    log_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)',
        handlers=[log_handler, logging.StreamHandler()]
    )

    logging.getLogger('weasyprint').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

def validate_website_config(site: Dict[str, Any]) -> bool:
    """Validate required website configuration parameters.

    Args:
        site: Website configuration dictionary

    Returns:
        bool: True if configuration is valid
    """
    required_fields = ['website_id', 'name', 'emails']

    for field in required_fields:
        if not site.get(field):
            logger.error(f"Missing required field: {field} in website configuration")
            return False

    return True

def get_website_settings(site: Dict[str, Any]) -> Tuple[str, str, str, List[str], bool, bool, str]:
    """Extract website settings from configuration."""
    return (
        site.get('lang', 'en'),
        site.get('frequency', 'daily'),
        site.get('email_template', 'email_template.html'),
        site.get('what_stats', ['stats', 'events', 'urls', 'referrers', 'browsers',
                               'oses', 'devices', 'countries']),
        site.get('send_pdf', True),
        site.get('generate_html', False),
        site.get('send_login_url', '')
    )

def load_translation(lang_code: str) -> Dict[str, Any]:
    """
    Load a translation file with automatic fallback for missing translations.

    Args:
        lang_code: Language code for the translation file

    Returns:
        Complete translation dictionary
    """
    try:
        return load_smart_translation(lang_code)
    except Exception as e:
        logger.error(f"Error loading translations: {e}")
        logger.warning("Falling back to English translations")
        return load_smart_translation('en')

def generate_report(website_name: str, context: Dict[str, Any],
                   email_template: str, generate_pdf: bool,
                   generate_html: bool) -> Tuple[str, Optional[str]]:
    """Generate HTML and optionally PDF reports."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(email_template)

    report = template.render(context)
    pdf_filename = None

    if generate_pdf:
        pdf_filename = f"pdf-files/{website_name.replace(' ', '_').lower()}_report.pdf"
        HTML(string=report).write_pdf(pdf_filename)
        logger.info(f"Report saved to {pdf_filename}")

    if generate_html:
        html_filename = f"html-files/{website_name.replace(' ', '_').lower()}_report.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Report saved to {html_filename}")

    return report, pdf_filename

def process_website(site: Dict[str, Any], now: datetime) -> None:
    """Process a single website to generate and send analytics reports."""
    try:
        if not validate_website_config(site):
            return

        # Extract settings
        lang, frequency, email_template, what_stats, generate_pdf, generate_html, login_url = get_website_settings(site)

        # Check scheduled time
        timer = site.get('email_time', "08:00")
        if int(timer.split(":")[0]) != now.hour:
            return

        website_id = site["website_id"]
        website_name = site["name"]
        recipients = site["emails"]
        send_day = site.get('send_day', [])
        top = site.get('top', 5)

        # Load translations
        translations = load_translation(lang)
        translations['frequency_options'] = frequency_options(frequency, translations)

        # Check if report should be sent
        if not should_send_report(frequency, send_day):
            return

        # Get date range and fetch data
        range_start, range_end = calculate_date_range(now, frequency)
        web_stats = get_umami_data(UMAMI_API_URL, BEARER_TOKEN, website_id,
                                 range_start, range_end, frequency, what_stats)

        # Prepare email content
        subject = translations['website_analytics_report_for'].format(
            frequency_options=translations['frequency_options'],
            website_name=website_name
        )

        login_url_text = translations['link_to_login'].format(login_url=login_url) if login_url else ""

        report_header = capitalize_sentences(
            translations["report_header"].format(
                website_name=website_name,
                frequency_text=translations[frequency],
                frequency_options_text=translations['frequency_options']
            )
        )

        comp_url = COMPANY.get('url', '#')
        comp_email = COMPANY.get('email', 'support@example.com')
        report_footer = capitalize_sentences(
            translations["report_footer"].format(
                comp_email=comp_email,
                comp_url=comp_url
            )
        )

        # Prepare template context
        context = {
            'lang': lang,
            'report_header': report_header,
            'report_footer': report_footer,
            'company': COMPANY,
            'frequency': frequency,
            'stats': web_stats.get("stats", {}),
            'mystats': web_stats,
            'what_stats': what_stats,
            'stat_type_mapping': type_mapping(),
            'website_name': website_name,
            'top': top,
            'translations': translations,
            'login_url_text': login_url_text
        }

        # Generate report
        report, pdf_filename = generate_report(
            website_name, context, email_template,
            generate_pdf, generate_html
        )

        # Send email (currently disabled)
        if report:
            send_email(subject, report, recipients, SMTP_CONFIG, pdf_filename)

    except Exception as e:
        logger.error(f"Error processing website {site.get('name', 'unknown')}: {str(e)}")
        logger.debug(traceback.format_exc())

def main() -> None:
    """Main execution function."""
    setup_logging()

    # Create necessary directories
    for folder in ['pdf-files', 'html-files']:
        check_create_dir(folder)

    # Authenticate with Umami API
    global BEARER_TOKEN
    BEARER_TOKEN = authenticate(UMAMI_API_URL, UMAMI_USERNAME, UMAMI_PASSWORD)

    if not BEARER_TOKEN:
        logger.error("Failed to authenticate with Umami API")
        exit(1)

    # Schedule and process reports
    schedule_reports(WEBSITES, process_website)

if __name__ == "__main__":
    main()
