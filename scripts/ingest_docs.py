from dotenv import load_dotenv
load_dotenv()

from rag.loader import load_documents
from rag.chunking import chunk_documents
from rag.embeddings import create_vectorstore
import os

DATA_DIR = "data/raw"
VECTORSTORE_DIR = "data/vectorstore"

if __name__ == "__main__":
    docs = load_documents(DATA_DIR)
    chunks = chunk_documents(docs)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    create_vectorstore(chunks, VECTORSTORE_DIR)

    print("✅ Vector store created successfully.")