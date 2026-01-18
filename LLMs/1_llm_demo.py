from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Optional safety check
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found. Check your .env file")

# Create Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7
)

# Invoke model
response = llm.invoke("What is the capital of India?")
print(response.content)
