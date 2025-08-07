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
    st.title("🧮 OpenAI Cost Calculator")
    st.markdown("---")
    
    try:
        # Import the cost calculator functionality
        from cost_prediction import calculate_cost, MODEL_PRICING, MODEL_PRICING_LINK
        import pandas as pd
        
        # Display model pricing
        st.markdown("### Model Pricing")
        pricing_data = []
        for model, prices in MODEL_PRICING.items():
            pricing_data.append({
                "Model": model,
                "Input ($/1M tokens)": f"${prices['input_per_1M']:.2f}",
                "Output ($/1M tokens)": f"${prices['output_per_1M']:.2f}",
                "Cache ($/1M tokens)": f"${prices['cache_per_1M']:.2f}"
            })
        
        pricing_df = pd.DataFrame(pricing_data)
        st.dataframe(pricing_df, use_container_width=True, hide_index=True)
        
        # Input section
        st.markdown("### ⚙️ Configuration Parameters")
        col1, col2 = st.columns(2)
        
        with col1:
            model = st.selectbox("**Select OpenAI Model**", list(MODEL_PRICING.keys()))
            num_users = st.number_input("**Number of Users**", min_value=1, value=10)
            max_chats = st.number_input("**Max Chats per User**", min_value=1, value=15)
        
        with col2:
            avg_input_tokens_per_chat = st.number_input("**Average Input Tokens per Chat**", min_value=1, value=1000)
            avg_output_tokens_per_chat = st.number_input("**Average Output Tokens per Chat**", min_value=1, value=50)
        
        if st.button("Calculate", type="primary", use_container_width=True):
            total_chats = num_users * max_chats
            total_input_tokens = total_chats * avg_input_tokens_per_chat
            total_output_tokens = total_chats * avg_output_tokens_per_chat
            
            cost = calculate_cost(model, total_input_tokens, total_output_tokens, 0)
            cost_rounded = round(cost, 2)
            
            # Results
            st.markdown("### 📊 Cost Analysis Results")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Chats", f"{total_chats:,}")
            with col2:
                st.metric("Input Tokens", f"{total_input_tokens:,}")
            with col3:
                st.metric("Output Tokens", f"{total_output_tokens:,}")
            with col4:
                st.metric("Estimated Cost", f"${cost_rounded:,.2f}")
                
    except Exception as e:
        st.error(f"Error loading Cost Calculator: {str(e)}")
        st.info("Please check that all required files are present.")

elif page == "Past Data Analysis":
    st.title("📊 Past Data Analysis")
    st.markdown("---")
    
    try:
        import pandas as pd
        import plotly.express as px
        
        # Check if data file exists
        if os.path.exists("merged_usage_cost.csv"):
            df = pd.read_csv("merged_usage_cost.csv")
            st.success(f"📊 Data loaded: {len(df)} records")
            
            # Show basic stats
            st.markdown("### Key Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_cost = df['amount_value'].sum() if 'amount_value' in df.columns else 0
                st.metric("Total Cost", f"${total_cost:.2f}")
            
            with col2:
                total_input = df['input_tokens'].sum() if 'input_tokens' in df.columns else 0
                st.metric("Total Input Tokens", f"{total_input:,.0f}")
            
            with col3:
                total_output = df['output_tokens'].sum() if 'output_tokens' in df.columns else 0
                st.metric("Total Output Tokens", f"{total_output:,.0f}")
            
            with col4:
                total_requests = df['num_model_requests'].sum() if 'num_model_requests' in df.columns else 0
                st.metric("Total Requests", f"{total_requests:,.0f}")
                
        else:
            st.warning("No data file found. Please ensure 'merged_usage_cost.csv' is available.")
            
    except Exception as e:
        st.error(f"Error loading Past Data Analysis: {str(e)}")
        st.info("Please check that all required files are present.")

# Add a simple test to ensure the app is working
st.sidebar.markdown("---")
st.sidebar.markdown("### Status")
st.sidebar.success("✅ App is running")