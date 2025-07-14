# Merges the csvs into one

import pandas as pd
import glob

usage_files = sorted(glob.glob("completions_usage_*.csv"))
cost_files = sorted(glob.glob("cost_*.csv"))

df_usage = pd.concat([pd.read_csv(f) for f in usage_files], ignore_index=True)
df_cost = pd.concat([pd.read_csv(f) for f in cost_files], ignore_index=True)

merged_df = pd.merge(
    df_usage,
    df_cost,
    on=["start_time", "end_time", "start_time_iso", "end_time_iso"],
    how="outer"
)

merged_df.to_csv("merged_usage_cost.csv", index=False)
print("Merged CSV saved to merged_usage_cost.csv")




