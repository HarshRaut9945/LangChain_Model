import streamlit as st
import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, Docx2txtLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA


# ---- Fix for Streamlit + async gRPC ----
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
nest_asyncio.apply()
# ----------------------------------------


# Load API Key
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ✅ Local embeddings (No quota issue)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


# Streamlit UI
st.set_page_config(page_title="RAG with LangChain", page_icon="🤖", layout="wide")
st.title("📂 RAG Q&A with Gemini")

uploaded_file = st.file_uploader(
    "Upload file...",
    type=["pdf", "txt", "docx"]   # ✅ fixed
)

if uploaded_file:
    with st.spinner("Processing file... Please wait"):

        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # 1️⃣ Load document
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif uploaded_file.name.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            loader = TextLoader(file_path)

        docs = loader.load()

        # 2️⃣ Split text
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(docs)

        # 3️⃣ Create vector store
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever()

        # 4️⃣ Create Retrieval QA chain
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

    st.success("File processed successfully ✅")

    # User Query
    user_query = st.text_input("Ask a question about the document")

    if user_query:
        with st.spinner("Fetching answer... 🤔"):
            response = qa({"query": user_query})

        # Show Answer
        st.subheader("💡 Answer")
        st.write(response["result"])

        # Show Sources
        st.subheader("📎 Sources")
        for i, doc in enumerate(response["source_documents"], 1):
            st.markdown(f"**Source {i}:** {doc.metadata}")
            st.write(doc.page_content[:300] + "...")
