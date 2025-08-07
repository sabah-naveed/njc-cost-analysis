# Cost calculator streamlit page

# to activate venv: source venv/bin/activate

import streamlit as st
from cost_prediction import calculate_cost, MODEL_PRICING, MODEL_PRICING_LINK
import pandas as pd
import numpy as np

# Page configuration is handled in the main app

# Main content area


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
    
