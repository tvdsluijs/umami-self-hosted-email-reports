def frequency_options(frequency, translations):
    if frequency == "day":
        return translations["daily"]
    elif frequency == "month":
        return translations["monthly"]
    elif frequency == "quarter":
        return translations["quarterly"]
    elif frequency == "year":
        return translations["yearly"]

    return ""
