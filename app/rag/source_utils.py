def extract_sources(docs):
    sources = []

    for doc in docs:
        meta = doc.metadata
        sources.append({
            "source": meta.get("source", "unknown"),
            "page": meta.get("page", None)
        })

    return sources