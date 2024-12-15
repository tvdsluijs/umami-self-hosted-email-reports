from datetime import timedelta

def calculate_date_range(now, frequency):
    try:
        # Convert now to epoch timestamp in milliseconds
        end_date = int(now.timestamp() * 1000)

        # Map frequency to timedelta days
        frequency_map = {
            "week": 7,
            "month": 30,
            "quarter": 90,
            "year": 365
        }

        if frequency not in frequency_map:
            raise ValueError(f"Invalid frequency: {frequency}")

        # Calculate start date
        new_datetime = now - timedelta(days=frequency_map[frequency])
        range_start = int(new_datetime.timestamp() * 1000)

        return range_start, end_date
    except Exception as e:
        print(f"Error calculating date range: {e}")
        return 0, 0
