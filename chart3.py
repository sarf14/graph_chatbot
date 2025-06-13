import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read and clean the CSV
file_path = "Graph Transaction (1).csv"
data = pd.read_csv(file_path)

# Strip whitespace from columns and values
data.columns = data.columns.str.strip()
data['period'] = data['period'].astype(str).str.strip()
for col in data.select_dtypes(include='object').columns:
    data[col] = data[col].astype(str).str.strip()

# Parameters to plot
categories = ['total_transactions', 'total_success', 'total_fail', 'customer_behaviour']

# Extract values for each period
def get_value(period, col):
    row = data[data['period'] == period]
    return int(row[col].values[0]) if not row.empty else 0

curr_week = [get_value('Current Week', cat) for cat in categories]
prev_week = [get_value('Previous Week', cat) for cat in categories]

# Bar positions
x = np.arange(len(categories))
bar_width = 0.35

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

bars1 = ax.bar(x - bar_width/2, curr_week, bar_width, color='#ff7f0e', label='Current Week')
bars2 = ax.bar(x + bar_width/2, prev_week, bar_width, color='#1f77b4', label='Previous Week')

# Add value labels
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f'{height}', ha='center', va='bottom', fontsize=10)

add_labels(bars1)
add_labels(bars2)

# Title, labels, and styling
ax.set_title('ATM Transaction Flow by Week', pad=20, fontsize=14, weight='bold')
plt.text(0.80, 0.92, "LIVE ATM COUNT - 22", transform=plt.gca().transAxes,
         ha='right', va='bottom', fontsize=12, color='black', weight='bold')
ax.set_ylabel('Count', fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels(['Total Transactions', 'Total Success', 'Total Fail', 'Customer Behaviour'], rotation=15)

ax.legend(loc='upper right')
plt.tight_layout()
plt.show()