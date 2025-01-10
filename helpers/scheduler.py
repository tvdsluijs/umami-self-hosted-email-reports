"""
📅 Scheduler Helper

This module provides functions to determine whether reports should be sent based
on scheduling frequencies and to execute the report generation process concurrently.

Functions:
- should_send_report: Determines if a report should be sent based on frequency and specified days.
- schedule_reports: Executes the report generation for multiple websites concurrently.
"""
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

def should_send_report(frequency, send_day):
    """
    Determines if a report should be sent based on the frequency and the current date.

    Args:
        frequency (str): The frequency of the report ("day", "week", "month", "quarter", "year").
        send_day (list): List of days for sending reports (e.g., ["mon", "wed"] for "day" or ["mon"] for "week").

    Returns:
        bool: True if a report should be sent, False otherwise.
    """
    now = datetime.now()
    day_name = now.strftime('%a').lower()  # Current day of the week (e.g., 'mon', 'tue')

    if frequency == 'day':
        # Send daily reports if no specific days are specified or today matches a specified day
        return not send_day or day_name in send_day
    elif frequency == 'week':
        # Send weekly reports on the specified day (default: first day of the week)
        return not send_day or day_name == send_day[0]
    elif frequency == 'month':
        # Send monthly reports on the 1st of the month
        return now.day == 1
    elif frequency == 'quarter':
        # Send quarterly reports on the 1st day of January, April, July, and October
        return now.day == 1 and now.month in [1, 4, 7, 10]
    elif frequency == 'year':
        # Send yearly reports on the 1st of January
        return now.day == 1 and now.month == 1
    return False

def schedule_reports(websites, process_website):
    """
    Schedules and processes report generation for multiple websites concurrently.

    Args:
        websites (list): A list of website configurations.
        process_website (function): A function to process an individual website.

    Execution:
        - Creates a thread pool to handle report generation concurrently.
        - Ensures errors during processing are caught and logged.
    """
    now = datetime.now()  # Capture the current datetime for consistent usage
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit report generation tasks for each website
        futures = [executor.submit(process_website, site, now) for site in websites]
        for future in futures:
            try:
                # Wait for task completion and handle any exceptions
                future.result()
            except Exception as e:
                logger.error(f"Error processing a website: {e}")
