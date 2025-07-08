import streamlit as st
from cost_prediction import calculate_cost, MODEL_PRICING, MODEL_PRICING_LINK

st.title("OpenAI Cost Analysis")

st.write("This app allows you to analyze the cost of using OpenAI models.")

model = st.selectbox("Select a model", list(MODEL_PRICING.keys()))

input_tokens = st.number_input("Input tokens", value=1000, min_value=0)
cache_tokens = st.number_input("Cache tokens", value=0, min_value=0)
output_tokens = st.number_input("Output tokens", value=300, min_value=0)

if st.button("Calculate cost"):
    cost = calculate_cost(model, input_tokens, output_tokens, cache_tokens)
    st.write(f"The cost of using {model} is {cost} USD")

st.write(f"For more information, see the [OpenAI pricing page]({MODEL_PRICING_LINK})")
