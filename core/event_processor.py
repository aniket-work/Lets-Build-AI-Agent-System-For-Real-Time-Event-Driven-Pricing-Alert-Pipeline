"""
Event Processor - Processes price events with AI agents
"""

import os
import yaml
import logging
from crewai import Crew, Process
from config.constants import (
    INPUT_QUEUE, OUTPUT_QUEUE,
    DESIRED_CATEGORIES, PRICE_DROP_THRESHOLD
)
from agents.agent_factory import create_pricing_analyst, create_notification_manager
from crewai import Task

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_prompts():
    """Load prompt templates from YAML file"""
    try:
        with open('config/prompts.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load prompts: {str(e)}")
        return {}


def process_event():
    """
    Process pricing events from the input queue using AI agents

    This function continuously monitors the input queue for new pricing events,
    and when one is found, it processes it with the AI agents to determine
    if an alert should be generated.
    """
    # Load prompt templates
    prompts = load_prompts()
    pricing_template = prompts.get('pricing_analysis_template', '')
    notification_template = prompts.get('notification_template', '')

    # Initialize agents
    pricing_analyst = create_pricing_analyst()
    notification_manager = create_notification_manager()

    logger.info("Event processor started")

    while True:
        try:
            if not INPUT_QUEUE.empty():
                event = INPUT_QUEUE.get()
                logger.info(f"Processing event for {event['product_name']}")

                # Format the pricing analysis prompt
                analysis_description = pricing_template.format(
                    product_name=event['product_name'],
                    category=event['category'],
                    our_price=event['our_price'],
                    competitor_price=event['competitor_price'],
                    desired_categories=DESIRED_CATEGORIES,
                    price_drop_threshold=PRICE_DROP_THRESHOLD * 100
                )

                # Create the pricing analysis task
                analysis_task = Task(
                    description=analysis_description,
                    agent=pricing_analyst,
                    expected_output="ALERT or IGNORE decision",
                )

                # Create the notification task
                notification_task = Task(
                    description=notification_template,
                    agent=notification_manager,
                    expected_output="Clear notification message with key details",
                    context=[analysis_task],
                )

                # Create and execute the crew
                crew = Crew(
                    agents=[pricing_analyst, notification_manager],
                    tasks=[analysis_task, notification_task],
                    verbose=True,
                    process=Process.sequential,
                )

                # Run the crew and get the result
                result = crew.kickoff()

                # If the result contains "ALERT", add it to the output queue
                if "ALERT" in result:
                    event["alert_details"] = result
                    OUTPUT_QUEUE.put(event)
                    logger.info(f"Alert generated for {event['product_name']}")

        except Exception as e:
            logger.error(f"Event processing error: {str(e)}")