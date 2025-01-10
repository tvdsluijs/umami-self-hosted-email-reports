"""
📊 Umami API Helper

This module provides functions to interact with the Umami Analytics API,
fetching and processing statistics for reporting.

Functions:
- validate_date_range: Ensures the provided date range is valid.
- fetch_stats: Performs an API request and returns the JSON response.
- determine_unit: Maps reporting frequency to the appropriate unit.
- get_umami_data: Fetches and processes data for specified statistics.
"""
import logging
import requests

logger = logging.getLogger(__name__)

def validate_date_range(range_start, range_end):
    """
    Validate that the date range is valid.

    Args:
        range_start (int): Start of the date range in epoch milliseconds.
        range_end (int): End of the date range in epoch milliseconds.

    Raises:
        ValueError: If the date range is invalid (e.g., start >= end or negative values).
    """
    if range_start >= range_end:
        raise ValueError("range_start must be less than range_end")
    if range_start < 0 or range_end < 0:
        raise ValueError("range_start and range_end must be non-negative")

def fetch_stats(url, headers, params):
    """
    Perform the API request and return JSON data.

    Args:
        url (str): The API endpoint URL.
        headers (dict): Headers for the API request (e.g., authorization).
        params (dict): Query parameters for the API request.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()

def determine_unit(frequency):
    """
    Determine the appropriate unit for the given frequency.

    Args:
        frequency (str): The report frequency ("day", "week", "month", "quarter", "year").

    Returns:
        str: The unit to use for the API request ("day", "month", or "year").

    Raises:
        ValueError: If the frequency is unsupported.
    """
    unit_mapping = {
        "day": "day",
        "week": "day",
        "month": "day",
        "quarter": "month",
        "year": "year",
    }
    if frequency not in unit_mapping:
        raise ValueError(f"Unsupported frequency: {frequency}")
    return unit_mapping[frequency]

def get_umami_data(api_url, token, website_id, range_start, range_end, frequency="week", what_stats=None):
    """
    Fetch and process data from Umami API for the requested statistics.

    Args:
        api_url (str): The base URL for the Umami API.
        token (str): The bearer token for authentication.
        website_id (str): The ID of the website in Umami.
        range_start (int): Start of the date range in epoch milliseconds.
        range_end (int): End of the date range in epoch milliseconds.
        frequency (str): The reporting frequency ("day", "week", etc.).
        what_stats (list): A list of stat types to retrieve (e.g., "urls", "countries").

    Returns:
        dict: A dictionary containing processed statistics.

    Raises:
        requests.exceptions.RequestException: For API request errors.
        ValueError: For invalid inputs like unsupported frequency or invalid date ranges.
    """
    validate_date_range(range_start, range_end)  # Ensure date range is valid
    unit = determine_unit(frequency)  # Map frequency to API unit

    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "startAt": range_start,
        "endAt": range_end,
        "unit": unit,
        "tz": "CET"
    }

    stats_url = f"{api_url}/websites/{website_id}/stats"
    metrics_url = f"{api_url}/websites/{website_id}/metrics"

    # Map stat types to their corresponding API endpoints and parameters
    stat_type_mapping = {
        "stats": {"url": stats_url, "type": None},
        "events": {"url": metrics_url, "type": "event"},
        "urls": {"url": metrics_url, "type": "url"},
        "referrers": {"url": metrics_url, "type": "referrer"},
        "browsers": {"url": metrics_url, "type": "browser"},
        "oses": {"url": metrics_url, "type": "os"},
        "devices": {"url": metrics_url, "type": "device"},
        "countries": {"url": metrics_url, "type": "country"}
    }

    mystats = {}
    try:
        for stat in what_stats or []:
            if stat not in stat_type_mapping:
                logger.error(f"Warning: Unsupported stat type '{stat}'. Skipping.")
                continue

            stat_config = stat_type_mapping[stat]
            params_with_type = {**params}
            if stat_config["type"]:
                params_with_type["type"] = stat_config["type"]

            # Fetch data from the API
            raw_data = fetch_stats(stat_config["url"], headers, params_with_type)

            # Process stats differently for general statistics
            if stat == "stats":
                mystats["stats"] = {
                    "pageviews": raw_data["pageviews"],
                    "visitors": raw_data["visitors"],
                    "visits": raw_data["visits"],
                    "bounces": raw_data["bounces"],
                    "totaltime": raw_data["totaltime"],
                }
            else:
                # Process other stats as label-value pairs
                mystats[stat] = [{"label": item["x"], "value": item["y"]} for item in raw_data]

        return mystats
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch stats for website {website_id}: {e}")
        return {}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {}
