import pandas as pd
import glob
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

CHATS_PER_USER_PER_DAY = 15
DAILY_USER_COUNTS = [100, 500, 1000, 2500, 5000]

def load_and_combine_data():
    csv_files = glob.glob('cost_*.csv')
    
    dfs = [pd.read_csv(file) for file in csv_files]
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # fix timestamps
    combined_df['start_time_iso'] = pd.to_datetime(combined_df['start_time_iso'])
    combined_df['end_time_iso'] = pd.to_datetime(combined_df['end_time_iso'])
    
    return combined_df

def analyze_costs(df):
    total_cost = df['amount_value'].sum()
    
    daily_costs = df.groupby(df['start_time_iso'].dt.date)['amount_value'].sum()
    
    monthly_costs = df.groupby(df['start_time_iso'].dt.to_period('M'))['amount_value'].sum()
    
    stats = {
        'total_cost': total_cost,
        'average_daily_cost': daily_costs.mean(),
        'max_daily_cost': daily_costs.max(),
        'min_daily_cost': daily_costs.min(),
        'days_with_usage': len(daily_costs[daily_costs > 0]),
        'total_days': len(daily_costs)
    }
    
    return stats, daily_costs, monthly_costs

def estimate_user_costs(avg_daily_cost, avg_chat_volume): 
    avg_cost_per_chat = avg_daily_cost / avg_chat_volume if avg_chat_volume > 0 else 0
    user_costs = {user_count: avg_cost_per_chat * CHATS_PER_USER_PER_DAY * user_count for user_count in DAILY_USER_COUNTS}
    return avg_cost_per_chat, user_costs

def plot_costs(daily_costs, monthly_costs):
    plt.style.use('seaborn-v0_8')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # plotting daily costs
    daily_costs.plot(kind='bar', ax=ax1)
    ax1.set_title('Daily API Usage Costs')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cost (USD)')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # plotting monthly costs
    monthly_costs.plot(kind='bar', ax=ax2)
    ax2.set_title('Monthly API Usage Costs')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Cost (USD)')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.savefig('cost_analysis.png')
    plt.close()

def main():
    df = load_and_combine_data()
    
    stats, daily_costs, monthly_costs = analyze_costs(df)

    avg_chat_volume = (stats['average_daily_cost'] / 0.003) 
    avg_cost_per_chat, user_costs = estimate_user_costs(stats['average_daily_cost'], avg_chat_volume)
    
    print("\nOPENAI API Usage Cost Analysis")
    print("=" * 50)
    print(f"Total Cost: ${stats['total_cost']:.2f}")
    print(f"Average Daily Cost: ${stats['average_daily_cost']:.2f}")
    print(f"Maximum Daily Cost: ${stats['max_daily_cost']:.2f}")
    print(f"Minimum Daily Cost: ${stats['min_daily_cost']:.2f}")
    print(f"Days with API Usage: {stats['days_with_usage']} out of {stats['total_days']} days")
    print("\nEstimated Cost per Chat: ${:.5f}".format(avg_cost_per_chat))
    print(f"\n--- Estimated Daily Cost per Number of Users (assuming {CHATS_PER_USER_PER_DAY} chats/user/day) ---")
    for users, cost in user_costs.items():
        print(f"{users} users → ${cost:.2f} per day")
    
    plot_costs(daily_costs, monthly_costs)
    print("\nCost analysis visualization has been saved as 'cost_analysis.png'")

if __name__ == "__main__":
    main() 