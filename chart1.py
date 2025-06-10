import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Load the data
data = pd.read_csv('durationdata_202506101519.csv')

# Separate current and previous week data
current_week = data[data['week_period'] == 'Current Week']
previous_week = data[data['week_period'] == 'Previous Week']

# Sort both datasets by down_type for consistent ordering
current_week = current_week.sort_values('down_type')
previous_week = previous_week.sort_values('down_type')

# Get the categories and values
categories = ['Previous Week', 'Current Week']
downtime_types = current_week['down_type'].unique()

# Create colors for each downtime type
colors = plt.cm.tab10.colors[:len(downtime_types)]

# Create a larger figure with more space
plt.figure(figsize=(14, 9))

# Plot the stacked bars with increased width
bar_width = 0.6
bottom_prev = 0
bottom_curr = 0

# Store small values for table
small_values = []

for i, down_type in enumerate(downtime_types):
    # Previous week values
    prev_val = previous_week[previous_week['down_type'] == down_type]['total_duration_hours'].values[0]
    bar_prev = plt.bar(0, prev_val, width=bar_width, bottom=bottom_prev, 
                      color=colors[i], label=down_type, edgecolor='white')
    bottom_prev += prev_val
    
    # Current week values
    curr_val = current_week[current_week['down_type'] == down_type]['total_duration_hours'].values[0]
    bar_curr = plt.bar(1, curr_val, width=bar_width, bottom=bottom_curr, 
                      color=colors[i], edgecolor='white')
    bottom_curr += curr_val

    # Add text labels for segments > 1 hour
    min_height_for_label = 1  # Minimum height in hours to show label
    prev_y = bottom_prev - prev_val/2
    curr_y = bottom_curr - curr_val/2
    
    if prev_val >= min_height_for_label:
        plt.text(0, prev_y, f'{prev_val:.2f}h', 
                ha='center', va='center', color='white', fontsize=10,
                bbox=dict(facecolor='black', alpha=0.3, boxstyle='round,pad=0.2'))
    else:
        small_values.append(('Previous ', down_type, prev_val))
    
    if curr_val >= min_height_for_label:
        plt.text(1, curr_y, f'{curr_val:.2f}h', 
                ha='center', va='center', color='white', fontsize=10,
                bbox=dict(facecolor='black', alpha=0.3, boxstyle='round,pad=0.2'))
    else:
        small_values.append(('Current ', down_type, curr_val))

# Add labels and title
plt.title('Downtime Comparison: Current Week vs Previous Week', pad=25, fontsize=16, weight='bold')
plt.xlabel('Week Period', labelpad=15, fontsize=12)
plt.ylabel('Total Duration (hours)', labelpad=15, fontsize=12)

# Create legend
legend = plt.legend(title='Downtime Types', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)

# Add total values on top of each bar
total_prev = previous_week['total_duration_hours'].sum()
total_curr = current_week['total_duration_hours'].sum()
plt.text(0, total_prev + 3, f'Total: {total_prev:.2f} hrs', 
        ha='center', fontsize=12, weight='bold')
plt.text(1, total_curr + 3, f'Total: {total_curr:.2f} hrs', 
        ha='center', fontsize=12, weight='bold')

# Adjust x-axis limits and ticks
plt.xlim(-0.5, 1.5)
plt.xticks([0, 1], categories, fontsize=12)

# Add grid lines
plt.grid(axis='y', alpha=0.3)

# Create table for small values
if small_values:
    # Prepare table data
    table_data = [['Week', 'Downtime Type', 'Hours']]
    for week, dtype, hours in small_values:
        table_data.append([week, dtype, f"{hours:.2f}"])
    
    # Add table below legend
    table = plt.table(cellText=table_data,
                     colLabels=None,
                     cellLoc='center',
                     bbox=[1.02, 0.1, 0.4, 0.3],  # x, y, width, height
                     colColours=['#f0f0f0']*3)
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#e0e0e0')
        cell.set_edgecolor('white')

plt.tight_layout(rect=[0, 0, 0.85, 1])  # Make space for legend and table
plt.show()