"""
🔒 Authentication Helper for Umami API

This module provides a function to authenticate with the Umami API and retrieve
a bearer token for subsequent API requests.

Functions:
- authenticate: Logs in to the Umami API and returns an authentication token.
"""
import logging
import requests

logger = logging.getLogger(__name__)

def authenticate(api_url: str, username: str, password: str):
    """
    Authenticates with the Umami API and retrieves a bearer token.

    Args:
        api_url (str): The base URL of the Umami API (e.g., "https://your-umami-instance").
        username (str): The username for the Umami account.
        password (str): The password for the Umami account.

    Returns:
        str: The bearer token if authentication is successful.

    Raises:
        SystemExit: If authentication fails due to missing parameters or API errors.
    """
    # Ensure required parameters are provided
    if not api_url or not username or not password:
        logger.error("Authentication failed: Missing required parameters.")
        exit(1)

    # Construct the login URL
    login_url = f"{api_url}/auth/login"
    payload = {"username": username, "password": password}

    try:
        # Send POST request to authenticate
        response = requests.post(login_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Extract the token from the response
        token = response.json().get("token")
        if not token:
            logger.error("Authentication failed: No token received.")
            exit(1)

        return token

    except requests.exceptions.RequestException as e:
        # Handle request errors
        logger.error(f"Failed to authenticate: {e}")
        exit(1)
