import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('Transaction flow.csv')
categories = ['Total Transactions', 'Total Success', 'Total Fail', 'Customer Behaviour']
prev_week = data.iloc[0]
curr_week = data.iloc[1]

# Set up the figure
fig, ax = plt.subplots(figsize=(12, 6))

# Positions for the bars (current week first, then space, then previous week)
x_positions = np.array([0, 1, 2, 3, 5, 6, 7, 8])  # Note gap at position 4

# Create bars - current week first (positions 0-3)
current_bars = ax.bar(x_positions[:4], 
                     [curr_week['total_transactions'], curr_week['total_success'],
                      curr_week['total_fail'], curr_week['customer_behaviour']],
                     width=0.6, color='#ff7f0e', label='Current Week')

# Then previous week (positions 5-8)
previous_bars = ax.bar(x_positions[4:], 
                      [prev_week['total_transactions'], prev_week['total_success'],
                       prev_week['total_fail'], prev_week['customer_behaviour']],
                      width=0.6, color='#1f77b4', label='Previous Week')

# Customize the plot
ax.set_title('Transaction Flow Comparison (Separated by Week)', pad=20)
ax.set_ylabel('Count')
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Set x-axis labels with gap between weeks
ax.set_xticks(x_positions)
ax.set_xticklabels(categories * 2)

# Add divider line between the two weeks
ax.axvline(x=4, color='gray', linestyle='--', alpha=0.5)

# Add value labels
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f'{int(height)}',
                ha='center', va='bottom')

add_labels(current_bars)
add_labels(previous_bars)

# Add legend and adjust layout
ax.legend(loc='upper right')
plt.tight_layout()
plt.show()