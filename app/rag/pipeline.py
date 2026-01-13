from rag.query_translation import translate_query
from rag.compression import compress_context
from rag.source_utils import extract_sources

def advanced_rag(question: str, retriever):
    # 1. Rewrite query
    rewritten_query = translate_query(question)

    # 2. Retrieve documents
    docs = retriever.invoke(rewritten_query)

    # 3. Compress context
    compressed_context = compress_context(question, docs)

    # 4. Track sources
    sources = extract_sources(docs)

    return {
        "rewritten_query": rewritten_query,
        "context": compressed_context,
        "sources": sources
    }