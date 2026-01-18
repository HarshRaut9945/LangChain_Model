from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

embedding=OpenAIEmbeddings(model='text-embedding-3-large',dimensions=32)

documnet=[
    "Delhi is the capital of India",
    "Kolata is the capital of West Bangal",
    "Paris is the capital of france"
]

result=embedding.embed_documents(documnet)

print(str(result))