"""
Pricing Intelligence Analyst Agent - Analyzes competitor price changes
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


def create_pricing_analyst():
    """
    Creates and configures a Pricing Intelligence Analyst agent specialized in
    analyzing competitor price changes and making actionable recommendations.

    Returns:
        Agent: Configured pricing analyst agent
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
        pricing_analyst = Agent(
            role="Pricing Intelligence Analyst",
            goal="Analyze competitor price changes and recommend strategic actions",
            backstory=(
                "Expert AI trained in market dynamics, competitive analysis, and pricing "
                "strategies across various product categories. Capable of identifying "
                "significant price movements and determining their potential impact on "
                "market position and sales performance."
            ),
            verbose=True,
            llm=llm,
            allow_delegation=False,
        )

        logger.info("Pricing Intelligence Analyst agent created successfully")
        return pricing_analyst

    except Exception as e:
        logger.error(f"Failed to create Pricing Intelligence Analyst agent: {str(e)}")
        raise