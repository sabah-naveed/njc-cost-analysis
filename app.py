# Cost calculator streamlit page

# to activate venv: source venv/bin/activate

import streamlit as st
from cost_prediction import calculate_cost, MODEL_PRICING, MODEL_PRICING_LINK
import pandas as pd
import numpy as np

st.sidebar.markdown("# Cost Calculator 🧮")
st.title("OpenAI Cost Calculator 🧮")

st.write("Estimate your OpenAI usage cost based on number of users and chats.")
st.write(f"For more information, see the [OpenAI pricing page]({MODEL_PRICING_LINK})")

# inputs 
model = st.selectbox("Select a model", list(MODEL_PRICING.keys()))
num_users = st.number_input("Number of users", min_value=1, value=10)
max_chats = st.number_input("Max chats per user", min_value=1, value=15)

avg_input_tokens_per_chat = st.number_input("Average input tokens per chat", min_value=1, value=1000)
avg_output_tokens_per_chat = st.number_input("Average output tokens per chat", min_value=1, value=300)
# cache_tokens = st.number_input("Cache tokens (optional)", value=0, min_value=0)
cache_tokens = 0

total_chats = num_users * max_chats
total_input_tokens = total_chats * avg_input_tokens_per_chat
total_output_tokens = total_chats * avg_output_tokens_per_chat

if st.button("Calculate cost"):
    cost = calculate_cost(model, total_input_tokens, total_output_tokens, cache_tokens)
    cost_rounded = round(cost, 2)
    st.write(f"Total chats (max): {total_chats}")
    st.write(f"Total input tokens: {total_input_tokens}")
    st.write(f"Total output tokens: {total_output_tokens}")
    st.write(f"The estimated cost of using {model} is {cost} -> {cost_rounded} USD")
