import pandas as pd
import dataframe_image as dfi

# Read CSV files
downtime_df = pd.read_csv('downtime top 5.csv')
success_df = pd.read_csv('Top 5 For Success.csv')

# Table 1: ATM Transaction Performance
table1 = success_df[['atm_id', 'total_transactions', 'success_rate']].copy()
table1.columns = ['ATM ID', 'Total Transactions', 'Success Rate (%)']
table1['Success Rate (%)'] = table1['Success Rate (%)'].map('{:.2f}%'.format)

# Table 2: ATM Downtime Analysis
table2 = downtime_df[['atm_id', 'total_downtime_hours', 'most_frequent_down_type']].copy()
table2.columns = ['ATM ID', 'Total Downtime (Hours)', 'Most Frequent Down']
table2['Total Downtime (Hours)'] = table2['Total Downtime (Hours)'].map('{:.4f}'.format)

# Style DataFrames for better appearance
styled_table1 = (
    table1.style
    .set_properties(**{'text-align': 'center', 'border': '1px solid black'})
    .set_table_styles([{'selector': 'th', 'props': [('border', '1px solid black')]}])
)

styled_table2 = (
    table2.style
    .set_properties(**{'text-align': 'center', 'border': '1px solid black'})
    .set_table_styles([{'selector': 'th', 'props': [('border', '1px solid black')]}])
)

# Export tables as images
dfi.export(styled_table1, "table1_transaction_performance.png", dpi=300)
dfi.export(styled_table2, "table2_downtime_analysis.png", dpi=300)

print("Tables saved as images: 'table1_transaction_performance.png' and 'table2_downtime_analysis.png'")