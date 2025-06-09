# config.py
import groq
from pandasai.llm.local_llm import LocalLLM

DB_NAME = "atmtransactionsdb"
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "3306"

GROQ_API_KEY = "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"
groq_client = groq.Client(api_key=GROQ_API_KEY)

llm = LocalLLM(api_base="http://localhost:11434/v1", model="llama3")
