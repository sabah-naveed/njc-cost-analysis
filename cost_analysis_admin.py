# Cost analysis with admin key

# update: not helpful because the only way you get cost data is blocked through API access #bigsad
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta, UTC
import time
import json 
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_ADMIN_KEY = os.getenv("openai_admin_key")

MODEL_PRICING = {
    "gpt-4o-mini": {
        "input_per_1M": 0.15,
        "cache_per_1M": 0.075,
        "output_per_1M": 0.60,
    },
    "gpt-4o": {
        "input_per_1M": 2.50,
        "cache_per_1M": 1.25,
        "output_per_1M": 10.00,
    },
    
}

MODEL_PRICING_LINK = "https://platform.openai.com/docs/pricing"

DAYS_AGO = 30

def get_data(url, params):
    headers = {
        "Authorization": f"Bearer {OPENAI_ADMIN_KEY}",
        "Content-Type": "application/json",
    }

    all_data = []

    page_cursor = None

    while True: 
        if page_cursor:
            params["page"] = page_cursor

        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data_json = response.json()
            all_data.extend(data_json.get("data", []))
            
            page_cursor = data_json["next_page"]

            if not page_cursor:
                break 
        else: 
            print(f"Error: {response.status_code}")
            break

    if all_data:
        print("Data retrieved successfully")
    else: 
        print("No data retrieved")

    return all_data

# def get_billing_usage(url, params):
#     headers = {
#         "Authorization": f"Bearer {OPENAI_ADMIN_KEY}",
#         "Content-Type": "application/json",
#     }
    
#     response = requests.get(url, headers=headers, params=params)
    
#     if response.status_code == 200:
#         data_json = response.json()
#         print("Billing data retrieved successfully")
#         return data_json
#     else:
#         print(f"Error retrieving billing data: {response.status_code}")
#         print(response.text)
#         return None
    
# def billing_to_dataframe(billing_data):
#     rows = []
    
#     for day in billing_data.get("daily_costs", []):
#         ts = day["timestamp"]
#         date = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
#         total_cost = day["total_cost"]
        
#         for item in day.get("line_items", []):
#             rows.append({
#                 "date": date,
#                 "model": item.get("model"),
#                 "input_tokens": item.get("n_context_tokens_total"),
#                 "output_tokens": item.get("n_generated_tokens_total"),
#                 "cost": item.get("cost"),
#                 "total_cost_for_day": total_cost,
#             })
    
#     df = pd.DataFrame(rows)
#     return df



def main():

    end_date = datetime.now(UTC).date()
    start_date = end_date - timedelta(days=DAYS_AGO)

    start_datetime = datetime.combine(start_date, datetime.min.time())
    start_time_unix = int(start_datetime.timestamp())

    # usage data
    url = "https://api.openai.com/v1/organization/usage/completions"

    params = {
        "start_time": start_time_unix,
        "bucket_width": "1d",
    }
    usage_data = get_data(url, params)
    print(usage_data)

    # # billing data 
    # url_billing = "https://api.openai.com/v1/dashboard/billing/usage"

    # params_billing = {
    #     "start_date": start_date.strftime("%Y-%m-%d"),
    #     "end_date": end_date.strftime("%Y-%m-%d"),
    # }

    # billing_data = get_billing_usage(url_billing, params_billing)
    
    # if billing_data:
    #     df_billing = billing_to_dataframe(billing_data)
    #     print(df_billing.head())
    # else:
    #     print("No billing data retrieved")


if __name__ == "__main__":
    main()

