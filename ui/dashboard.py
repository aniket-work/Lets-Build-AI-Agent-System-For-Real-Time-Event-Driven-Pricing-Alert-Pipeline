"""
Streamlit Dashboard - Real-time monitoring interface
"""

import json
import streamlit as st
from config.constants import INPUT_QUEUE, OUTPUT_QUEUE


def load_settings():
    """Load application settings from JSON file"""
    try:
        with open('config/settings.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load settings: {str(e)}")
        return {}


def streamlit_app():
    """
    Real-time monitoring dashboard built with Streamlit

    This function defines the layout and functionality of the
    Streamlit dashboard for monitoring pricing events and alerts.
    """
    settings = load_settings()
    app_settings = settings.get('application', {})

    # Application title and header
    st.title(app_settings.get('name', "AI Pricing Monitor"))
    st.write(app_settings.get('description', "Real-time competitor price monitoring with AI-powered analysis"))

    # Settings display
    with st.expander("System Settings"):
        st.json(settings)

    # Dashboard layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("All Price Events")

        # Display all events from the input queue
        if INPUT_QUEUE.empty():
            st.info("No price events detected yet")
        else:
            for event in list(INPUT_QUEUE.queue):
                with st.container():
                    st.write(f"**{event['timestamp']} - {event['product_name']}**")
                    st.write(f"Category: {event['category']}")
                    st.write(f"Our Price: ${event['our_price']}")
                    st.write(f"Competitor Price: ${event['competitor_price']}")
                    st.divider()

    with col2:
        st.subheader("Critical Alerts")

        # Display alerts from the output queue
        alerts = list(OUTPUT_QUEUE.queue)
        if not alerts:
            st.success("No alerts detected")
        else:
            for alert in alerts:
                # Calculate price difference percentage
                price_diff = ((alert['our_price'] - alert['competitor_price']) / alert['our_price']) * 100

                # Create an alert box
                with st.container():
                    if price_diff > 0:
                        st.error(f"🚨 {alert['product_name']} Alert!")
                    else:
                        st.warning(f"⚠️ {alert['product_name']} Alert!")

                    st.write(f"**Price Difference:** {abs(price_diff):.1f}%")
                    st.write(f"**Category:** {alert['category']}")
                    st.write(f"**Our Price:** ${alert['our_price']}")
                    st.write(f"**Competitor Price:** ${alert['competitor_price']}")

                    # Show the alert details
                    with st.expander("View Alert Details"):
                        st.write(alert.get('alert_details', ''))

                    st.divider()

    # Auto-refresh the dashboard
    refresh_interval = settings.get('monitoring', {}).get('refresh_interval', 1.0)
    st.empty()
    st.experimental_rerun()