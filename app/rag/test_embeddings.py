# test_rag.py
import logging
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from rag.config import VECTORSTORE_DIR
from loader import load_documents
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

# -----------------------------
# 1️⃣ PDF-ek betöltése
# -----------------------------
data_dir = Path("data/raw")
documents = load_documents(data_dir)
print(f"Betöltött dokumentumok száma: {len(documents)}")

if not documents:
    print("Nincsenek dokumentumok. Ellenőrizd a PDF mappát!")
    exit()

# -----------------------------
# 2️⃣ Chunkolás
# -----------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", "; ", ", ", " "]
)
chunks = splitter.split_documents(documents)
print(f"Chunkok száma: {len(chunks)}")

# -----------------------------
# 3️⃣ Chunk szűrés (relevánsak)
# -----------------------------
def is_good_chunk(doc):
    text = doc.page_content.lower()
    keywords = ["parametric", "design", "model", "feature", "update", "parameter"]
    return len(text) > 50 and any(k in text for k in keywords)

filtered_chunks = [c for c in chunks if is_good_chunk(c)]
print(f"Szűrt chunkok száma: {len(filtered_chunks)}")

if not filtered_chunks:
    print("Nincsenek releváns chunkok. Finomítsd a szűrést!")
    exit()

# -----------------------------
# 4️⃣ Embeddingek
# -----------------------------
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# -----------------------------
# 5️⃣ Chroma vectorstore
# -----------------------------
vectorstore_dir = Path("vectorstore")
vectorstore_dir.mkdir(exist_ok=True)

vectordb = Chroma(
    persist_directory=str(vectorstore_dir),
    embedding_function=embeddings
)

# Dokumentumok hozzáadása
vectordb.add_documents(filtered_chunks)
vectordb.persist()
print("Vectorstore létrehozva és mentve.")

# -----------------------------
# 6️⃣ Teszt: similarity search
# -----------------------------
query = "parametric design"
results = vectordb.similarity_search(query)
print(f"Talált chunkok száma a '{query}' kifejezésre: {len(results)}")

if results:
    print("\nElső találat preview:")
    print(results[0].page_content[:500])