import streamlit as st
import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader,TextLoader,Docx2txtLoader,PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import retrieval_qa


# ---- Fix for Streamlit + async gRPC ----
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
nest_asyncio.apply()
# ----------------------------------------



#step 1
load_dotenv()

llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash',google_api_key=os.getenv('GOOGLE_API_KEY'))

embeddings=GoogleGenerativeAIEmbeddings(model='models/embedding-001',google_api_key=os.getenv('GOOGLE_API_KEY'))

# step 2: stramlit App
st.set_page_config(page_title="RAG with LangChain", page_icon="🤖", layout="wide")
st.title("📂 RAG Q&A with Gemini")

uploaded_file=st.file_uploader("uploaded file...",type=['.pdf','.txt','.dock'])


if uploaded_file:
    with st.spinner('File Uploading...Please wait'):
        file_path=f"temp_{uploaded_file.name}"
        with open(file_path,'wb') as f:
            f.write(uploaded_file.read())



        # Rag Step

        #step 1
           # Load file
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif uploaded_file.name.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            loader = TextLoader(file_path)
        docs=loader.load()

        # step 2:
        splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
        chunks=splitter.split_documents(docs)
