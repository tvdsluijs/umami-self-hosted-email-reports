import requests

def validate_date_range(range_start, range_end):
    """Validate that the date range is valid."""
    if range_start >= range_end:
        raise ValueError("range_start must be less than range_end")
    if range_start < 0 or range_end < 0:
        raise ValueError("range_start and range_end must be non-negative")

def fetch_stats(url, headers, params):
    """Perform the API request and return JSON data."""
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def determine_unit(frequency):
    """Determine the appropriate unit based on the frequency."""
    unit_mapping = {
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
    """
    validate_date_range(range_start, range_end)
    unit = determine_unit(frequency)

    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "startAt": range_start,
        "endAt": range_end,
        "unit": unit,
        "tz": "CET"
    }

    stats_url = f"{api_url}/websites/{website_id}/stats"
    metrics_url = f"{api_url}/websites/{website_id}/metrics"

    # Map stat types to their corresponding "type" parameter or endpoint
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
                print(f"Warning: Unsupported stat type '{stat}'. Skip gettign data.")
                continue

            stat_config = stat_type_mapping[stat]
            params_with_type = {**params}
            if stat_config["type"]:
                params_with_type["type"] = stat_config["type"]

            raw_data = fetch_stats(stat_config["url"], headers, params_with_type)

            # Process stats differently to include `prev`
            if stat == "stats":
                mystats["stats"] = {
                    "pageviews": raw_data["pageviews"],
                    "visitors": raw_data["visitors"],
                    "visits": raw_data["visits"],
                    "bounces": raw_data["bounces"],
                    "totaltime": raw_data["totaltime"],
                }
            else:
                mystats[stat] = [{"label": item["x"], "value": item["y"]} for item in raw_data]

        return mystats
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch stats for website {website_id}: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
