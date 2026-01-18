from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv


load_dotenv()


model=ChatGoogleGenerativeAI(model='gemini-2.5-flash',google_api_key=os.getenv('GOOGLE_API_KEY'))

user_querry="How far earth is from sun"

output=model.invoke(user_querry)

print(output.content)
