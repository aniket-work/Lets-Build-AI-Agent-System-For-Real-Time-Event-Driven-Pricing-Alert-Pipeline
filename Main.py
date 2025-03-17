#!/usr/bin/env python3
"""
AI Pricing Monitor - Main Entry Point

This is the main entry point for the AI Pricing Monitor application,
which provides real-time competitor price monitoring with AI-powered analysis.
"""

import os
import threading
import streamlit as st
from queue import Queue
from dotenv import load_dotenv

# Internal imports
from core.connectivity import check_network_connection, verify_openai_key
from core.price_emitter import price_emitter
from core.event_processor import process_event
from ui.dashboard import streamlit_app
from config.constants import INPUT_QUEUE, OUTPUT_QUEUE


def initialize_system():
    """Initialize system components and verify requirements"""
    # Load environment variables
    load_dotenv()

    try:
        # Verify connectivity and API keys
        check_network_connection()
        verify_openai_key()
        return True
    except Exception as e:
        st.error(f"Initialization failed: {str(e)}")
        return False


def main():
    """Main application entry point"""
    # Initialize queues for inter-thread communication
    global INPUT_QUEUE, OUTPUT_QUEUE

    if not initialize_system():
        st.stop()

    try:
        # Start background threads
        threading.Thread(target=price_emitter, daemon=True).start()
        threading.Thread(target=process_event, daemon=True).start()

        # Start Streamlit app
        streamlit_app()

    except KeyboardInterrupt:
        print("System shutdown requested")
    except Exception as e:
        st.error(f"Critical error: {str(e)}")


if __name__ == "__main__":
    main()