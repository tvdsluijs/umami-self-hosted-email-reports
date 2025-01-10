
import logging
logger = logging.getLogger(__name__)

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
        logger.error(f"Error getting frequency options: {e}")
        return ""
    except Exception as e:
        logger.error(f"Error getting frequency options: {e}")
        return ""
