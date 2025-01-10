"""
🔄 Smart Translation Loader

This module handles translation file loading with automatic fallback to sample.json
for missing translations. It ensures all required keys are present by filling gaps
with English translations from the sample file.

Functions:
- load_base_translation: Load the sample/base translation file
- merge_translations: Merge missing translations from base into target
- load_smart_translation: Main function to load and complete translations
"""
import os
import json
import logging
from typing import Dict, Union
from copy import deepcopy

logger = logging.getLogger(__name__)

def load_base_translation(locale_dir: str = "locale") -> Dict:
    """
    Load the base translation file (sample.json).

    Args:
        locale_dir (str): Directory containing translation files

    Returns:
        dict: Base translation dictionary
    """
    base_path = os.path.join(locale_dir, "sample.json")
    try:
        with open(base_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Base translation file not found: {base_path}")
        raise FileNotFoundError(f"Required base translation file not found: {base_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in base translation file: {e}")
        raise ValueError(f"Invalid JSON in base translation file: {e}")

def merge_translations(base: Dict, translation: Dict) -> Dict:
    """
    Recursively merge translations, filling in missing keys from base.

    Args:
        base (dict): Base translation dictionary
        translation (dict): Target translation dictionary

    Returns:
        dict: Merged translation dictionary
    """
    result = deepcopy(translation)

    for key, value in base.items():
        if key not in result:
            result[key] = deepcopy(value)
            logger.info(f"Added missing translation for key: {key}")
        elif isinstance(value, dict) and isinstance(result[key], dict):
            result[key] = merge_translations(value, result[key])

    return result

def load_smart_translation(lang_code: str, locale_dir: str = "locale") -> Dict:
    """
    Load a translation file and auto-fill missing translations from sample.json.

    Args:
        lang_code (str): Language code for the translation file
        locale_dir (str): Directory containing translation files

    Returns:
        dict: Complete translation dictionary
    """
    # First load the base translation
    base_translations = load_base_translation(locale_dir)

    # If requesting English or sample, return base translations
    if lang_code in ['en', 'sample']:
        return base_translations

    # Try to load the requested translation file
    translation_path = os.path.join(locale_dir, f"{lang_code}.json")
    try:
        with open(translation_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
    except FileNotFoundError:
        logger.warning(f"Translation file not found for {lang_code}, using English")
        return base_translations
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in translation file {lang_code}: {e}")
        return base_translations

    # Merge translations, filling in gaps from base
    complete_translations = merge_translations(base_translations, translations)

    # Log if any translations were added
    if complete_translations != translations:
        logger.info(f"Auto-filled missing translations for {lang_code}")

    return complete_translations

def verify_translation_structure(translations: Dict, base: Dict, path: str = "") -> bool:
    """
    Verify that a translation dictionary has all required keys and proper value types.

    Args:
        translations (dict): Translation dictionary to verify
        base (dict): Base translation dictionary to compare against
        path (str): Current key path for nested dictionaries

    Returns:
        bool: True if structure is valid, False otherwise
    """
    for key, base_value in base.items():
        current_path = f"{path}.{key}" if path else key

        if key not in translations:
            logger.error(f"Missing translation key: {current_path}")
            return False

        if isinstance(base_value, dict):
            if not isinstance(translations[key], dict):
                logger.error(f"Invalid type for key {current_path}: expected dict")
                return False
            if not verify_translation_structure(translations[key], base_value, current_path):
                return False

    return True
