import pandas as pd
import dataframe_image as dfi

# Read and clean column names
success_df = pd.read_csv('Top 5 Success (1).csv')
success_df.columns = success_df.columns.str.strip().str.replace(' +', '_', regex=True)

downtime_df = pd.read_csv('Top 5 Down.csv')
downtime_df.columns = downtime_df.columns.str.strip().str.replace(' +', '_', regex=True)

# Table 1: ATM Transaction Performance
table1 = success_df[['atm_id', 'total_transactions', 'success_rate']].copy()
table1['success_rate'] = table1['success_rate'].map('{:.2f}%'.format)

# Table 2: ATM Downtime Analysis
table2 = downtime_df[['atm_id', 'total_downtime_hours', 'most_frequent_down_type']].copy()
table2['total_downtime_hours'] = table2['total_downtime_hours'].map('{:.4f}'.format)

# Style Table 1
styled_table1 = (
    table1.style
    .set_properties(**{'text-align': 'center', 'border': '1px solid black'})
    .set_table_styles([{'selector': 'th', 'props': [('border', '1px solid black')]}])
    .set_caption("ATM Transaction Performance")
)

# Style Table 2
styled_table2 = (
    table2.style
    .set_properties(**{'text-align': 'center', 'border': '1px solid black'})
    .set_table_styles([{'selector': 'th', 'props': [('border', '1px solid black')]}])
    .set_caption("ATM Downtime Analysis")
)

# Export as images
dfi.export(styled_table1, "table1_transaction_performance.png", dpi=300)
dfi.export(styled_table2, "table2_downtime_analysis.png", dpi=300)

print("✅ Tables saved as images: 'table1_transaction_performance.png' and 'table2_downtime_analysis.png'")