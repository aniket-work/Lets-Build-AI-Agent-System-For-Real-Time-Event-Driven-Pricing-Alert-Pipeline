"""
Network connectivity and API verification module
"""

import os
import json
import logging
import requests
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_settings():
    """Load application settings from JSON file"""
    try:
        with open('config/settings.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load settings: {str(e)}")
        raise


def check_network_connection():
    """
    Verifies network connectivity to the OpenAI API

    Returns:
        bool: True if connection is successful

    Raises:
        ConnectionError: If connection fails
    """
    settings = load_settings()
    api_url = settings['api']['openai']['health_check_url']
    timeout = settings['api']['openai']['timeout']

    try:
        response = requests.get(api_url, timeout=timeout)
        if response.status_code == 200:
            logger.info("Network connection to OpenAI API successful!")
            return True
        else:
            logger.warning(f"Connection test failed with status code: {response.status_code}")
            raise ConnectionError(f"Connection test failed with status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Network connection error: {str(e)}")
        raise ConnectionError(f"Network connection error: {str(e)}")


def verify_openai_key():
    """
    Verifies that the OpenAI API key is valid and working

    Returns:
        bool: True if API key is valid

    Raises:
        ValueError: If API key is missing
        ConnectionError: If API key verification fails
    """
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        raise ValueError("OPENAI_API_KEY not found in .env file")

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Connection test"}],
            max_tokens=5
        )
        logger.info("OpenAI API key verification successful!")
        return True
    except Exception as e:
        logger.error(f"API key verification failed: {str(e)}")
        raise ConnectionError(f"API key verification failed: {str(e)}")