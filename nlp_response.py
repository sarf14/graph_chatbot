# nlp_response.py
from config import groq_client

def get_response_for_query_result(question, data):
    prompt = f"""
    Make sure:
    - You use the WEEK() or YEARWEEK() function to group records based on standard calendar weeks.
    - Provide a clear, natural language summary of the weekly totals (e.g., "Week 6 (Feb 5–Feb 11): 200 transactions").
    - Ignore any weeks that fall outside February.
    - Use only actual calendar weeks, not custom manual groupings.
    - Base the grouping on the `inserted_on` column, which is of date or datetime type.
    - If asked daywise please use dates for each day of the month individually

    You are a helpful assistant. The user asked: "{question}" 

    The database returned the following data: {data}

    Frame the response in simple, conversational English. Be friendly and avoid technical terms.
    """
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
