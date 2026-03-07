import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Load API key from .env
load_dotenv()

# =========================
# 1. LOAD DOCUMENTS
# =========================
def load_documents(docs_path="docs"):
    print(f"📂 Loading documents from {docs_path}...")

    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"Directory '{docs_path}' not found")

    loader = DirectoryLoader(
        path=docs_path,
        glob="*.txt",
        loader_cls=lambda path: TextLoader(
            path,
            encoding="utf-8",
            autodetect_encoding=True
        ),
    )

    documents = loader.load()

    if not documents:
        raise ValueError("No .txt files found in docs folder")

    print(f"✅ Loaded {len(documents)} documents")

    # Preview first docs
    for i, doc in enumerate(documents[:2]):
        print(f"\n📄 Document {i+1}")
        print("Source:", doc.metadata.get("source"))
        print("Length:", len(doc.page_content))
        print("Preview:", doc.page_content[:120])

    return documents

# =========================
# 2. SPLIT INTO CHUNKS
# =========================
def split_documents(documents, chunk_size=1000, chunk_overlap=100):
    print("\n✂️ Splitting documents into chunks...")

    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(documents)

    print(f"✅ Created {len(chunks)} chunks")

    # Preview chunks
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i+1} ---")
        print("Source:", chunk.metadata.get("source"))
        print("Length:", len(chunk.page_content))
        print("Text:", chunk.page_content[:150])

    return chunks
# =========================
# 3. CREATE VECTOR STORE
# =========================
def create_vector_store(chunks, persist_directory="db/chroma_db"):
    print("\n🧠 Creating Gemini embeddings + ChromaDB...")

    # Gemini embedding model (latest)
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="text-embedding-004"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space": "cosine"},
    )

    print(f"✅ Vector DB stored at: {persist_directory}")
    return vectorstore

# =========================
# MAIN PIPELINE
# =========================
def main():
    print("🚀 Gemini RAG Ingestion Started\n")

    documents = load_documents("docs")
    chunks = split_documents(documents)
    create_vector_store(chunks)

    print("\n🎉 Ingestion completed successfully!")


if __name__ == "__main__":
    main()
