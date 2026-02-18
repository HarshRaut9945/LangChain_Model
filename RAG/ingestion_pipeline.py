import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path="docs"):
    print(f"📂 Loading documents from {docs_path}...")
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The directory {docs_path} does not exist.")
    loader = DirectoryLoader(
        path=docs_path,
        glob="*.txt",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8", autodetect_encoding=True)
    )
    documents = loader.load()

    if len(documents) == 0:
        raise FileNotFoundError(f"No .txt files found in {docs_path}")

    for i, doc in enumerate(documents[:2]):
        print(f"\n📄 Document {i+1}")
        print("Source:", doc.metadata.get("source"))
        print("Length:", len(doc.page_content))
        print("Preview:", doc.page_content[:100])
    return documents


def main():
    print("🚀 Ingestion started\n")

    documents = load_documents("docs")

    print(f"\n✅ Total documents loaded: {len(documents)}")


if __name__ == "__main__":
    main()
