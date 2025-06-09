import pandas as pd

# Step 1: Load the CSV
df = pd.read_csv('./data2.csv')

# Step 2: Fix the datetime format
# Assume your bad format is like '25-04-2025 14:30' or something messy
# Let's parse and reformat it properly
df['inserted_on'] = pd.to_datetime(df['inserted_on'], errors='coerce')  # Parses it
df['inserted_on'] = df['inserted_on'].dt.strftime('%Y-%m-%d %H:%M:%S')  # Correct MySQL format

# Step 3: Save it back
df.to_csv('FIXED_DATA5.csv', index=False)

print("Datetime format fixed and saved as 'FIXED_DATA.csv'.")
