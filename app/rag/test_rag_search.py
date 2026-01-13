from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

VECTORSTORE_DIR = "vectorstore"  # Győződj meg, hogy a helyes path

# Embedding és vectorstore betöltése
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectordb = Chroma(
    persist_directory=VECTORSTORE_DIR,
    embedding_function=embeddings
)

# Teszt query
query = "parametric design"
results = vectordb.similarity_search(query, k=5)

print(f"Talált chunkok száma: {len(results)}\n")
for i, r in enumerate(results):
    print(f"--- CHUNK {i} ---")
    print(r.page_content[:500], "\n")