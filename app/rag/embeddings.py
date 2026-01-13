from loader import load_documents
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# --- PDF-ek betöltése ---
pdf_path = Path(__file__).parent / "data" / "raw"
documents = load_documents(str(pdf_path))
print(f"Betöltött dokumentumok száma: {len(documents)}")

if not documents:
    print("Nincs PDF dokumentum betöltve, kilépés.")
    exit(1)

# --- Chunkolás ---
splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"Chunkok száma: {len(chunks)}")

if not chunks:
    print("Nincs chunk létrehozva, kilépés.")
    exit(1)

# --- Szűrés (relevancia) ---
def is_good_chunk(doc):
    text = doc.page_content.lower()
    return len(text) > 50 and any(
        w in text for w in ["parametric", "design", "model", "feature", "update"]
    )

chunks = [c for c in chunks if is_good_chunk(c)]
print(f"Szűrt chunkok száma: {len(chunks)}")

if not chunks:
    print("Szűrés után nincs releváns chunk, kilépés.")
    exit(1)

# --- Embeddings ---
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# --- Chroma vectorstore ---
vectorstore_dir = Path(__file__).parent / "vectorstore"
vectorstore_dir.mkdir(exist_ok=True)

vectordb = Chroma(
    persist_directory=str(vectorstore_dir),
    embedding_function=embeddings
)

# --- Dokumentumok hozzáadása ---
vectordb.add_documents(chunks)
vectordb.persist()

print(f"Vectorstore létrehozva: {len(chunks)} chunk mentve")