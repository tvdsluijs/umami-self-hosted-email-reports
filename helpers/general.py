import os
import logging
logger = logging.getLogger(__name__)

def capitalize_sentences(text):
    """
    Capitalizes the first letter of each sentence in a given text.

    Args:
        text (str): The input string containing sentences.

    Returns:
        str: The modified string with each sentence capitalized.
    """
    try:
        # Ensure the input is a string
        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        # Split the text into sentences by '. ' (assumes sentences end with period + space)
        sentences = text.split('. ')

        # Capitalize each sentence and store them in a list
        capitalized_sentences = [s.capitalize() for s in sentences if s]  # Ignore empty sentences

        # Join the capitalized sentences back into a single string with '. ' separator
        final_text = '. '.join(capitalized_sentences)

        return final_text

    except TypeError as e:
        logger.error(f"Error: {e}")
        return ""
    except Exception as e:
        # Handle any unexpected error
        logger.error(f"An unexpected error occurred: {e}")
        return ""

def type_mapping(type_name:str = ""):
    """
    Maps a given type name to its corresponding value in the type_map dictionary.

    Args:
        type_name (str): The type name to map.

    Returns:
        str: The mapped value from the type_map dictionary, or the original type_name if not found.
    """
    type_map = {
        "url": "pages",
        "referrer": "referrers",
        "browser": "browsers",
        "os": "oses",
        "device": "devices",
        "country": "countries",
        "event": "events"
    }


    if type_name:
        return type_map.get(type_name, type_name)
    else:
        return type_map

def check_create_dir(directory):
    """
    Checks if a directory exists, and creates it if it does not.

    Args:
        directory (str): The path of the directory to check and create.

    Returns:
        bool: True if the directory exists or was created successfully, False otherwise.
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)  # Attempt to create the directory
            logger.info(f"Directory created: {directory}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {e}")
            return False
    else:
        logger.info(f"Directory already exists: {directory}")
        return True
