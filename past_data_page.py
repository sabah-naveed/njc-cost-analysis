import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import numpy as np

st.markdown("# Past Data Analysis 🕰️")
st.sidebar.markdown("# Past Data Analysis 🕰️")

# load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("merged_usage_cost.csv")
        
        df['start_time_iso'] = pd.to_datetime(df['start_time_iso'])
        df['end_time_iso'] = pd.to_datetime(df['end_time_iso'])
        
        return df
    except FileNotFoundError:
        st.error("merged_usage_cost.csv not found. Please run csv_combiner.py first.")
        return None

df = load_data()

if df is not None:
    # Date range picker
    st.header("📅 Select Date Range")
    
    # Get min and max dates from data
    min_date = df['start_time_iso'].min().date()
    max_date = df['end_time_iso'].max().date()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
    with col2:
        end_date = st.date_input(
            "End Date", 
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )
    
    # Filter data by date range
    mask = (df['start_time_iso'].dt.date >= start_date) & (df['end_time_iso'].dt.date <= end_date)
    filtered_df = df[mask].copy()
    
    if not filtered_df.empty:
        st.success(f"📊 Data loaded: {len(filtered_df)} records from {start_date} to {end_date}")
        
        # Main statistics
        st.header("📈 Key Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_cost = filtered_df['amount_value'].sum()
            st.metric("Total Cost", f"${total_cost:.2f}")
        
        with col2:
            total_input_tokens = filtered_df['input_tokens'].sum()
            st.metric("Total Input Tokens", f"{total_input_tokens:,.0f}")
        
        with col3:
            total_output_tokens = filtered_df['output_tokens'].sum()
            st.metric("Total Output Tokens", f"{total_output_tokens:,.0f}")
        
        with col4:
            total_requests = filtered_df['num_model_requests'].sum()
            st.metric("Total Requests", f"{total_requests:,.0f}")
        
        # Model breakdown
        st.header("🤖 Usage by Model")
        
        model_stats = filtered_df.groupby('model').agg({
            'amount_value': 'sum',
            'input_tokens': 'sum',
            'output_tokens': 'sum',
            'num_model_requests': 'sum'
        }).round(2)
        
        model_stats['total_tokens'] = model_stats['input_tokens'] + model_stats['output_tokens']
        model_stats['cost_per_1k_tokens'] = (model_stats['amount_value'] / (model_stats['total_tokens'] / 1000)).round(4)
        
        st.dataframe(model_stats, use_container_width=True)
        
        # Cost trend over time
        st.header("💰 Cost Trend")
        
        daily_costs = filtered_df.groupby(filtered_df['start_time_iso'].dt.date)['amount_value'].sum().reset_index()
        daily_costs.columns = ['date', 'cost']
        
        fig_cost = px.line(daily_costs, x='date', y='cost', 
                          title='Daily Cost Trend',
                          labels={'date': 'Date', 'cost': 'Cost (USD)'})
        fig_cost.update_layout(height=400)
        st.plotly_chart(fig_cost, use_container_width=True)
        
        # Token usage trend
        st.header("📊 Token Usage Trend")
        
        daily_tokens = filtered_df.groupby(filtered_df['start_time_iso'].dt.date).agg({
            'input_tokens': 'sum',
            'output_tokens': 'sum'
        }).reset_index()
        daily_tokens.columns = ['date', 'input_tokens', 'output_tokens']
        
        fig_tokens = px.line(daily_tokens, x='date', y=['input_tokens', 'output_tokens'],
                            title='Daily Token Usage',
                            labels={'date': 'Date', 'value': 'Tokens', 'variable': 'Token Type'})
        fig_tokens.update_layout(height=400)
        st.plotly_chart(fig_tokens, use_container_width=True)
        
        # Request trend over time
        st.header("📈 Daily Request Trend")
        
        daily_requests = filtered_df.groupby(filtered_df['start_time_iso'].dt.date)['num_model_requests'].sum().reset_index()
        daily_requests.columns = ['date', 'requests']
        
        fig_requests = px.line(daily_requests, x='date', y='requests', 
                              title='Daily Request Count',
                              labels={'date': 'Date', 'requests': 'Number of Requests'})
        fig_requests.update_layout(height=400)
        st.plotly_chart(fig_requests, use_container_width=True)
        
        # Model usage pie chart
        st.header("🍰 Model Distribution")
        
        model_costs = filtered_df.groupby('model')['amount_value'].sum()
        
        fig_pie = px.pie(values=model_costs.values, names=model_costs.index,
                        title='Cost Distribution by Model')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Detailed data table
        st.header("📋 Detailed Data")
        
        # Show only non-null rows for better readability
        display_df = filtered_df.dropna(subset=['amount_value', 'input_tokens'])
        
        if not display_df.empty:
            st.dataframe(display_df, use_container_width=True)
            
            # Download button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download filtered data as CSV",
                data=csv,
                file_name=f"usage_data_{start_date}_to_{end_date}.csv",
                mime="text/csv"
            )
        else:
            st.info("No data with usage information in the selected date range.")
    
    else:
        st.warning("No data found for the selected date range.")
else:
    st.error("Unable to load data. Please ensure merged_usage_cost.csv exists.")

