import pandas as pd

# Load the CSV
file_path = './FIXED_DATA3.csv'
df = pd.read_csv(file_path)

# Drop rows where 'inserted_on' is empty or NaN
df_cleaned = df.dropna(subset=['inserted_on'])

# Also drop if it's an empty string (sometimes it's not NaN but just '')
df_cleaned = df_cleaned[df_cleaned['inserted_on'].astype(str).str.strip() != '']

# Save the cleaned file (optional)
cleaned_file_path = './CleanedData.csv'
df_cleaned.to_csv(cleaned_file_path, index=False)

print(f"Rows with empty 'inserted_on' removed and saved to {cleaned_file_path}")
