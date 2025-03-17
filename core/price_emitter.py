"""
Price Emitter module - Simulates competitor price changes
"""

import time
import random
import logging
import json
from datetime import datetime
from config.constants import (
    INPUT_QUEUE, PRODUCTS,
    MIN_EMITTER_DELAY, MAX_EMITTER_DELAY,
    PRICE_VARIATION_MIN, PRICE_VARIATION_MAX
)

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
        return None


def price_emitter():
    """
    Simulates competitor price changes at random intervals.
    Generates price events and places them in the input queue.
    """
    settings = load_settings()
    if settings and not settings.get('simulation', {}).get('enabled', True):
        logger.info("Price emitter simulation disabled in settings")
        return

    logger.info("Starting price emitter simulation")

    while True:
        try:
            # Choose a random product
            product = random.choice(PRODUCTS)

            # Generate a competitor price with some variation
            competitor_price = product["our_price"] * random.uniform(
                PRICE_VARIATION_MIN,
                PRICE_VARIATION_MAX
            )

            # Create the price event
            event = {
                "product_id": product["id"],
                "product_name": product["name"],
                "category": product["category"],
                "our_price": product["our_price"],
                "competitor_price": round(competitor_price, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Add to the queue
            INPUT_QUEUE.put(event)
            logger.debug(f"Added pricing event to queue: {event['product_name']}")

            # Wait for a random interval before the next event
            time.sleep(random.uniform(MIN_EMITTER_DELAY, MAX_EMITTER_DELAY))

        except Exception as e:
            logger.error(f"Price emitter error: {str(e)}")
            # Continue even after error, but with a brief delay
            time.sleep(1.0)