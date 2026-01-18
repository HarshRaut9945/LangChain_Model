from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 


load_dotenv()

# Safety check
assert os.getenv("GROQ_API_KEY"), "GROQ_API_KEY not found!"

# Initialize Chat Model
chat_model = ChatGroq(
    model="llama-3.1-8b-instant",  # Chat-capable model
    temperature=0.7
)
response = chat_model.invoke("Suggest me 7 best romantic pakistani drama with higest imdb raiting ")
print(response.content )