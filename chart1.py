import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Load and clean the data
data = pd.read_csv('.csv')
data.columns = data.columns.str.strip()  # Clean column names
data['down_type'] = data['down_type'].str.strip()  # Clean values
data['week_period'] = data['week_period'].str.strip()

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

# Create a larger figure
plt.figure(figsize=(14, 9))
bar_width = 0.6
bottom_prev = 0
bottom_curr = 0
small_values = []

for i, down_type in enumerate(downtime_types):
    # Previous week values
    prev_val = previous_week[previous_week['down_type'] == down_type]['total_duration_hours'].values
    prev_val = prev_val[0] if len(prev_val) else 0
    bar_prev = plt.bar(0, prev_val, width=bar_width, bottom=bottom_prev, 
                       color=colors[i], label=down_type, edgecolor='white')
    bottom_prev += prev_val

    # Current week values
    curr_val = current_week[current_week['down_type'] == down_type]['total_duration_hours'].values
    curr_val = curr_val[0] if len(curr_val) else 0
    bar_curr = plt.bar(1, curr_val, width=bar_width, bottom=bottom_curr, 
                       color=colors[i], edgecolor='white')
    bottom_curr += curr_val

    # Add text labels for segments > 1 hour
    min_height = 1
    if prev_val >= min_height:
        plt.text(0, bottom_prev - prev_val/2, f'{prev_val:.2f}h',
                 ha='center', va='center', color='white', fontsize=10,
                 bbox=dict(facecolor='black', alpha=0.3, boxstyle='round,pad=0.2'))
    else:
        small_values.append(('Previous     ', down_type, prev_val))
    
    if curr_val >= min_height:
        plt.text(1, bottom_curr - curr_val/2, f'{curr_val:.2f}h',
                 ha='center', va='center', color='white', fontsize=10,
                 bbox=dict(facecolor='black', alpha=0.3, boxstyle='round,pad=0.2'))
    else:
        small_values.append(('Current    ', down_type, curr_val))

# Labels and title
plt.title('Downtime Comparison: Current Week vs Previous Week', pad=25, fontsize=16, weight='bold')
plt.title('Downtime Comparison: Current Week vs Previous Week', pad=25, fontsize=16, weight='bold')

# Add "LIVE ATM COUNT - 27" in the top-right corner
plt.text(0.98, 0.92, "LIVE ATM COUNT - 22", transform=plt.gca().transAxes,
         ha='right', va='bottom', fontsize=12, color='black', weight='bold')
plt.xlabel('Week Period', labelpad=15, fontsize=12)
plt.ylabel('Total Duration (hours)', labelpad=15, fontsize=12)
plt.legend(title='Downtime Types', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)

# Total values on top
plt.text(0, bottom_prev + 3, f'Total: {bottom_prev:.2f} hrs', ha='center', fontsize=12, weight='bold')
plt.text(1, bottom_curr + 3, f'Total: {bottom_curr:.2f} hrs', ha='center', fontsize=12, weight='bold')

# Axis setup
plt.xlim(-0.5, 1.5)
plt.xticks([0, 1], categories, fontsize=12)
plt.grid(axis='y', alpha=0.3)

# Add table for small values
if small_values:
    table_data = [['Week', 'Downtime Type', 'Hours']]
    for week, dtype, hours in small_values:
        table_data.append([week, dtype, f"{hours:.2f}"])
    table = plt.table(cellText=table_data, colLabels=None, cellLoc='center',
                      bbox=[1.02, 0.1, 0.4, 0.3],
                      colColours=['#f0f0f0'] * 3)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#e0e0e0')
        cell.set_edgecolor('white')

plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.show()
