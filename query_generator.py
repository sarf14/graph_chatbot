# query_generator.py
from config import groq_client
from schema_utils import load_schema

def get_groq_response(question):
    schema = load_schema()
    prompt = f"""
You are an expert in making SQL queries which align with MARIA DB syntax.
When asked about filtering based on number of days, use the DAY() function on the 'inserted_on' column to filter for specific day intervals like 1 to 10, 11 to 20, etc.
Use only the columns in the schema provided below.

Schema:
{schema}

**Rules:**
- Return only the SQL query.
- Use proper JOINs, GROUP BY, etc. as needed.
- No formatting like ```sql

Example:
Question: How many albums are in the database?
Answer: SELECT COUNT(*) FROM album;

Question: {question}
Answer:
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
