import pandas as pd
import re

# Load the CSV
df = pd.read_csv('./FebmonthTransactionData.csv')

# Fix datetime with regex
def fix_datetime(x):
    if pd.isna(x) or not isinstance(x, str):
        return x
    x = x.strip()
    # Allow one or more spaces (\s+)
    match = re.match(r'^(\d{2})-(\d{2})-(\d{4})\s+(\d{2}:\d{2}:\d{2})$', x)
    if match:
        day, month, year, time_part = match.groups()
        return f"{year}-{month}-{day} {time_part}"
    return x  # Return as-is if doesn't match

df['inserted_on'] = df['inserted_on'].apply(fix_datetime)

# Save the corrected CSV
df.to_csv('FIXED_DATA09.csv', index=False)

print("Datetime formatting corrected (even with multiple spaces) and saved.")
