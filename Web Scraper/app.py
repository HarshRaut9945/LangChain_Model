import streamlit as st
from langchain_community.document_loaders import WebBaseLoader,SeleniumURLLoader,UnstructuredURLLoader

# ---------------- USER AGENTS LIST ----------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
]
#sidebar
st.sidebar.title('⚙️ Scraper Options')
scraper_choice = st.sidebar.selectbox("Choose Scraper",("Unstructured Loader", "Selenium Loader", "WebBase Loader"))
user_agent = st.sidebar.selectbox("Choose User Agent", USER_AGENTS)

#Main area
st.set_page_config(page_title='Langchain Scaper',layout='wide')
st.title('Lanchain Scrapper')

url=st.text("Enter Website URL...")

if st.button('Scrap Content'):
    pass