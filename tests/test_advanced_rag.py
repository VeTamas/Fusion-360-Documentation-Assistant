from dotenv import load_dotenv
load_dotenv()

from rag.embeddings import load_vectorstore
from rag.retriever import get_retriever
from rag.pipeline import advanced_rag

VECTORSTORE_PATH = "data/vectorstore"

def main():
    vs = load_vectorstore(VECTORSTORE_PATH)
    retriever = get_retriever(vs)

    question = "How does parametric design work in Fusion 360?"

    result = advanced_rag(question, retriever)

    print("\n--- ADVANCED RAG TEST ---\n")
    print("Original question:")
    print(question)

    print("\nRewritten query:")
    print(result["rewritten_query"])

    print("\nCompressed context (first 500 chars):")
    print(result["context"][:500])

    print("\nSources:")
    for src in result["sources"]:
        print(src)


if __name__ == "__main__":
    main()