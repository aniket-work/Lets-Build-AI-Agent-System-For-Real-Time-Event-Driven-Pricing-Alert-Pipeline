"""
System constants for the AI Pricing Monitor
"""

from queue import Queue

# Communication queues
INPUT_QUEUE = Queue()
OUTPUT_QUEUE = Queue()

# Monitored product categories
DESIRED_CATEGORIES = ["electronics", "appliances", "smart home"]

# Alert thresholds
PRICE_DROP_THRESHOLD = 0.05  # 5%

# Sample products (in production, this would come from a database)
PRODUCTS = [
    {"id": 1, "name": "4K Smart TV", "category": "electronics", "our_price": 799.99},
    {"id": 2, "name": "Blender", "category": "appliances", "our_price": 89.99},
    {"id": 3, "name": "Smart Thermostat", "category": "smart home", "our_price": 149.99},
]

# API request configuration
API_REQUEST_TIMEOUT = 30  # seconds

# Price emitter configuration
MIN_EMITTER_DELAY = 0.5  # seconds
MAX_EMITTER_DELAY = 1.5  # seconds
PRICE_VARIATION_MIN = 0.8  # 80% of our price
PRICE_VARIATION_MAX = 1.1  # 110% of our price