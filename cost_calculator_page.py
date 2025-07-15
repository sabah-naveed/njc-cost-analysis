# Cost calculator streamlit page

# to activate venv: source venv/bin/activate

import streamlit as st
from cost_prediction import calculate_cost, MODEL_PRICING, MODEL_PRICING_LINK
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="OpenAI Cost Calculator",
    page_icon="🧮",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.markdown("# Cost Calculator 🧮")
    st.markdown("---")
    
    # Information section in sidebar
    st.markdown("### About This Calculator")
    st.markdown("""
    This cost calculator helps you estimate the monthly cost of using OpenAI's API for the **Transit AI project**.
    
    **What it calculates:**
    - **Model selection**: Choose from different OpenAI models (GPT-4o, GPT-4o-mini, etc.)
    - **Usage parameters**: Number of users, maximum chats per user, and token usage
    - **Token consumption**: Input and output tokens per chat interaction
    
    **Note**: Input tokens are typically much higher than output tokens due to context window and model instructions.
    """)
    
    st.markdown("### How to Use")
    st.markdown("""
    1. Select your preferred OpenAI model
    2. Enter your expected number of users and chats per user
    3. Specify average token usage per chat
    4. Click "Calculate cost" to see your estimated monthly expense
    """)
    
    st.markdown("---")
    st.markdown("### Model Pricing")
    
    # Create pricing table
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
    
    st.markdown("---")
    st.markdown("### Resources")
    st.markdown(f"📖 [OpenAI Pricing]({MODEL_PRICING_LINK})")


st.title("🧮 OpenAI Cost Calculator")
st.markdown("---")

col1, col2 = st.columns([2, 1])

# Input section
st.markdown("### ⚙️ Configuration Parameters")

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Model & Users")
    model = st.selectbox("**Select OpenAI Model**", list(MODEL_PRICING.keys()), help="Choose the model that best fits your needs")
    num_users = st.number_input("**Number of Users**", min_value=1, value=10, help="Expected number of active users")
    max_chats = st.number_input("**Max Chats per User**", min_value=1, value=15, help="Maximum number of chats per user per month")

with col2:
    st.markdown("#### Token Usage")
    avg_input_tokens_per_chat = st.number_input("**Average Input Tokens per Chat**", min_value=1, value=1000, help="Includes context, instructions, and user messages")
    avg_output_tokens_per_chat = st.number_input("**Average Output Tokens per Chat**", min_value=1, value=50, help="Model's response tokens")
    cache_tokens = 0  # hidden


if st.button("Calculate", type="primary", use_container_width=True):
    total_chats = num_users * max_chats
    total_input_tokens = total_chats * avg_input_tokens_per_chat
    total_output_tokens = total_chats * avg_output_tokens_per_chat
    
    cost = calculate_cost(model, total_input_tokens, total_output_tokens, cache_tokens)
    cost_rounded = round(cost, 2)
    
    # Results section
    st.markdown("### 📊 Cost Analysis Results")
    
    # Create metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Chats (Max)", f"{total_chats:,}")
    
    with col2:
        st.metric("Input Tokens", f"{total_input_tokens:,}")
    
    with col3:
        st.metric("Output Tokens", f"{total_output_tokens:,}")
    
    with col4:
        st.metric("Estimated Cost", f"${cost_rounded:,.2f}")
    
    # Detailed breakdown
    st.markdown("---")
    st.markdown("#### 💰 Cost Breakdown")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**Model Used**: {model}")
        st.warning(f"**Total Cost**: ${cost_rounded:,.2f} USD")
    
    with col2:
        st.info(f"**Cost per Chat**: ${cost/total_chats:.4f}")
        st.info(f"**Cost per User**: ${cost/num_users:.4f}")
    
