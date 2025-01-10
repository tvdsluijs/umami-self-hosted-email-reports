"""
📅 Date Range Calculator

This module provides a utility function to calculate date ranges for
analytics reports based on a specified frequency.

Functions:
- calculate_date_range: Computes the start and end dates for a report based on frequency.
"""
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

def calculate_date_range(now, frequency):
    """
    Calculates the start and end date range for analytics reports.

    Args:
        now (datetime): The current date and time.
        frequency (str): The report frequency, one of "day", "week", "month", "quarter", "year".

    Returns:
        tuple: A tuple containing the start and end dates as epoch timestamps in milliseconds.

    Raises:
        ValueError: If the frequency is invalid.
        Exception: For other errors during calculation.
    """
    try:
        # Convert the current datetime to an epoch timestamp in milliseconds
        end_date = int(now.timestamp() * 1000)

        # Map each frequency to a corresponding timedelta in days
        frequency_map = {
            "day": 1,
            "week": 7,
            "month": 30,
            "quarter": 90,
            "year": 365
        }

        # Validate the frequency input
        if frequency not in frequency_map:
            raise ValueError(f"Invalid frequency: {frequency}")

        # Calculate the start date based on the frequency
        new_datetime = now - timedelta(days=frequency_map[frequency])
        range_start = int(new_datetime.timestamp() * 1000)

        return range_start, end_date

    except Exception as e:
        # Handle unexpected errors and return default values
        logger.error(f"Error calculating date range: {e}")
        return 0, 0
