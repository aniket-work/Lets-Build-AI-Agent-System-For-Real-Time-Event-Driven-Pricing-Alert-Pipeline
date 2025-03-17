"""
Notification Manager Agent - Generates clear communications for internal teams
"""

import logging
from crewai import Agent
from langchain_openai import ChatOpenAI
import os
from config.constants import API_REQUEST_TIMEOUT

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_notification_manager():
    """
    Creates and configures a Notification Manager agent specialized in
    generating clear, actionable notifications for internal teams.

    Returns:
        Agent: Configured notification manager agent
    """
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=os.environ["OPENAI_API_KEY"],
            temperature=0.3,
            request_timeout=API_REQUEST_TIMEOUT
        )

        # Create the agent
        notification_manager = Agent(
            role="Notification Manager",
            goal="Generate clear, actionable communications for internal teams",
            backstory=(
                "Specialist in business communications with expertise in crafting "
                "concise yet comprehensive messages that effectively convey critical "
                "information and recommended actions to relevant stakeholders."
            ),
            verbose=True,
            llm=llm,
            allow_delegation=False,
        )

        logger.info("Notification Manager agent created successfully")
        return notification_manager

    except Exception as e:
        logger.error(f"Failed to create Notification Manager agent: {str(e)}")
        raise