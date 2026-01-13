from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents):
    """
    Dokumentumok feldarabolása RAG-hoz.
    - Chunk size kisebb, overlap mérsékelt
    - Szűrés rugalmasabb
    """
    # 1️⃣ Splitter finomhangolása
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,       # kisebb chunkok
        chunk_overlap=50,     # mérsékelt átfedés
        separators=["\n\n", "\n", ". ", "; ", ", ", " "]
    )

    # 2️⃣ Chunkolás
    chunks = splitter.split_documents(documents)
    print(f"Összes chunk a splitter után: {len(chunks)}")

    # 3️⃣ Jó chunkok szűrése
    KEYWORDS = [
        "parameter", "design", "model", "change", "update", "feature",
        "component", "sketch", "constraint", "assembly", "timeline", "history"
    ]

    def is_good_chunk(text: str) -> bool:
        text_lower = text.lower()
        # Rugalmas hossz: 50 karaktertől
        return len(text_lower) >  10 and any(word in text_lower for word in KEYWORDS)

    filtered_chunks = [c for c in chunks if is_good_chunk(c.page_content)]
    print(f"Szűrt, releváns chunkok száma: {len(filtered_chunks)}")

    # 4️⃣ Preview ellenőrzés (debug, opcionális)
    for i, chunk in enumerate(filtered_chunks[:5]):
        print(f"\n--- CHUNK {i} ---\n")
        print(chunk.page_content[:500])

    return filtered_chunks