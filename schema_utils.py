# schema_utils.py
import pandas as pd
import os

def load_schema(schema_file='./new_schema_2.csv'):
    if os.path.exists(schema_file):
        schema_df = pd.read_csv(schema_file)
        schema = "\n".join([
            f"Table: {row['TABLE_NAME']}, Column: {row['COLUMN_NAME']}, Type: {row['DATA_TYPE']}, "
            f"Nullable: {row['IS_NULLABLE']}, Key: {row['COLUMN_KEY']}, Default: {row['COLUMN_DEFAULT']}, "
            f"Extra: {row['EXTRA']}"
            for _, row in schema_df.iterrows()
        ])
        return schema
    else:
        return "Schema file not found."
