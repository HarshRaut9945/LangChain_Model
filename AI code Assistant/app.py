import streamlit as st
from langchain_community.document_loaders import Docx2txtLoader,PyMuPDFLoader
import os
import tempfile
from langchain_client import LangChainClient

st.set_page_config(page_title='AI code Assistant',layout='wide')

if "message" not in st.session_state:
    st.session_state.message=[]
if "mode" not in st.session_state:
    st.session_state.mode=None
if "uplaoded_texts" not in st.session_state:
    st.session_state.uploaded_texts={}

st.title("AI code Assistant (Lanchain + Gemni)")

#sidebar
st.sidebar.header("Select File")

uploaded_files=st.sidebar.file_uploader(
    "Choose files",
    accept_multiple_files=True,
    type=[
        "py", "js", "ts", "java", "cpp", "c", "html", "css", "json",
        "go", "rb", "php", "cs", "txt", "md", "docx", "pdf"
    ]
)

st.sidebar.header("Choose Mode")
mode=st.sidebar.selectbox(
    "Choose Mode",
   [
       "General", "Code Analysis", "Code Generator", "Debugger",
        "Code Guide", "Optimization", "Explain Code",
        "Project Builder", "Documentation"
   ],
   index=0
)
st.session_state.mode=mode

LC=LangChainClient(mode=st.session_state.mode)
st.caption(f"Assistant is running in   **{mode}**")