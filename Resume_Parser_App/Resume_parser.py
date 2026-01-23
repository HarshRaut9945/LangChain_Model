import os
from dotenv import load_dotenv
import json
import  streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

from langchain_core.prompts import PromptTemplate


load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

PROMPT_TEMPLATE = """
You are an expert resume parser. Given the resume text, extract the following fields and return a single valid JSON object:

{{
  "Name": "...",
  "Email": "...",
  "Phone": "...",
  "LinkedIn": "...",
  "Skills": [...],
  "Education": [...],
  "Experience": [...],
  "Projects": [...],
  "Certifications": [...],
  "Languages": [...]
}}

Rules:
- If a field cannot be found, set its value to "No idea".
- Return ONLY valid JSON (no extra commentary).
- Keep lists as arrays, and keep Experience/Projects as arrays of short strings.

Resume text:
{text}
"""
prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["text"])

def extract_docs_file(uploaded_file):
    tempt_path=f"temp_{uploaded_file.name}"

    with open(tempt_path,'wb') as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith('.pdf'):
        loader=PyPDFLoader(tempt_path)

    elif uploaded_file.name.endswith('.docx'):
        loader= Docx2txtLoader(tempt_path)
    elif uploaded_file.name.endswith(".txt"):
        loader = TextLoader(tempt_path)

    else:
        return None
    return loader.load()


def main():
    st.title("📄 Resume Parser — LangChain")
    uploaded_file=st.file_uploader("Upload Resume ", type=["pdf","docx","text"])

    if uploaded_file:
        with st.spinner("Loading Resume....."):
           docs=extract_docs_file(uploaded_file)
           if not docs:
               st.error("Unsported file type")
               return
           
        st.subheader("Ectracted Text (previous)")
        preview_text = "\n\n".join([d.page_content for d in docs])[:4000]
        st.text_area("Preview", value=preview_text, height=200)


        if st.button("Ask LLM"):
            with st.spinner("Sending to llm...."):
                formated_promt=prompt.format(text=preview_text)
                response=llm.invoke(formated_promt)
                try:
                    parsed_json = json.loads(response.content)
                    st.json(parsed_json)
                except json.JSONDecodeError:
                    st.write(response.content)  

                st.write(response.content)




#python main
if __name__=="__main__":
    main()