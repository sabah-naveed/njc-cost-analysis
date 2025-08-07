import streamlit as st
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="NJC Cost Analysis",
    page_icon="🧮",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("🧮 NJC Cost Analysis")
st.sidebar.markdown("---")

# Page selection
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Cost Calculator", "Past Data Analysis"]
)

# Main content area
if page == "Cost Calculator":
    try:
        # Import and run the cost calculator page
        exec(open("cost_calculator_page.py").read())
    except Exception as e:
        st.error(f"Error loading Cost Calculator: {str(e)}")
        st.info("Please check that all required files are present.")

elif page == "Past Data Analysis":
    try:
        # Import and run the past data page
        exec(open("past_data_page.py").read())
    except Exception as e:
        st.error(f"Error loading Past Data Analysis: {str(e)}")
        st.info("Please check that all required files are present.")

# Add a simple test to ensure the app is working
st.sidebar.markdown("---")
st.sidebar.markdown("### Status")
st.sidebar.success("✅ App is running")