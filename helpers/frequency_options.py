
def frequency_options(frequency, translations):
    try:
        if frequency == "day":
            return translations["daily"]
        elif frequency == "month":
            return translations["monthly"]
        elif frequency == "quarter":
            return translations["quarterly"]
        elif frequency == "year":
            return translations["yearly"]

        return ""
    except KeyError as e:
        print(f"Error getting frequency options: {e}")
        return ""
    except Exception as e:
        print(f"Error getting frequency options: {e}")
        return ""
