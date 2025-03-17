"""
Agent Factory - Creates and configures AI agents
"""

import os
import yaml
import logging
from crewai import Agent
from langchain_openai import ChatOpenAI
from config.constants import API_REQUEST_TIMEOUT

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_agent_configs():
    """Load agent configurations from YAML file"""
    try:
        with open('config/agents.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load agent configs: {str(e)}")
        return {}


def create_llm():
    """Create and configure the language model"""
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=os.environ["OPENAI_API_KEY"],
            temperature=0.3,
            request_timeout=API_REQUEST_TIMEOUT
        )
        return llm
    except Exception as e:
        logger.error(f"LLM initialization failed: {str(e)}")
        raise


def create_pricing_analyst():
    """
    Create and configure the Pricing Intelligence Analyst agent

    Returns:
        Agent: Configured pricing analyst agent
    """
    configs = load_agent_configs()
    analyst_config = configs.get('pricing_analyst', {})

    llm = create_llm()

    return Agent(
        role=analyst_config.get('role', "Pricing Intelligence Analyst"),
        goal=analyst_config.get('goal', "Analyze competitor price changes and recommend actions"),
        backstory=analyst_config.get('backstory', "Expert AI trained in market dynamics and pricing strategies."),
        verbose=analyst_config.get('verbose', True),
        llm=llm,
        allow_delegation=analyst_config.get('allow_delegation', False),
    )


def create_notification_manager():
    """
    Create and configure the Notification Manager agent

    Returns:
        Agent: Configured notification manager agent
    """
    configs = load_agent_configs()
    manager_config = configs.get('notification_manager', {})

    llm = create_llm()

    return Agent(
        role=manager_config.get('role', "Notification Manager"),
        goal=manager_config.get('goal', "Generate clear communications for internal teams"),
        backstory=manager_config.get('backstory', "Specialist in business communications."),
        verbose=manager_config.get('verbose', True),
        llm=llm,
        allow_delegation=manager_config.get('allow_delegation', False),
    )