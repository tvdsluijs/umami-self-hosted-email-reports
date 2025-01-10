"""
⚙️ Configuration Loader

This module provides a utility function to load and parse JSON configuration files
used by the Umami Email Reports script.

Functions:
- load_config: Loads and returns the contents of a configuration file as a dictionary.
"""
import logging
import json

logger = logging.getLogger(__name__)

def load_config(file_path):
    """
    Loads a JSON configuration file and returns its contents.

    Args:
        file_path (str): The path to the JSON configuration file.

    Returns:
        dict: The parsed contents of the JSON file.

    Raises:
        SystemExit: If the file is not found or cannot be loaded.
    """
    try:
        # Open and parse the configuration file
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Handle missing file error
        print(f"Configuration file {file_path} not found. Exiting.")
        exit(1)
