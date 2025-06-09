# db_utils.py
import mysql.connector
import pandas as pd
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME

def execute_sql_query(sql):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()

        return pd.DataFrame(rows, columns=columns) if rows else pd.DataFrame()
    except mysql.connector.Error as e:
        return f"SQL Error: {e}"
