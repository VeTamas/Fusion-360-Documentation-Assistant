# RAG Debug Skill

Use this skill when the RAG pipeline returns errors or poor answers.

## Diagnose steps

1. Check ChromaDB collection size:
   docker exec rag_app python -c "from langchain_chroma import Chroma; from langchain_google_genai import GoogleGenerativeAIEmbeddings; import os; db = Chroma(persist_directory='/app/app/rag/vectorstore', embedding_function=GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001')); print(db._collection.count())"

2. Test embedding query:
   docker exec rag_app python -c "
   import sys; sys.path.insert(0, '/app/app')
   from rag.qa import answer_with_rag
   result = answer_with_rag('what is parametric design')
   print(result)
   "

3. Check app logs:
   docker logs rag_app --tail 50

4. Check DB connection:
   docker exec rag_app python -c "from db.session import engine; print(engine.url)"

## Common fixes
- Empty vectorstore: re-run embeddings.py with GOOGLE_API_KEY set
- DB table missing: docker exec rag_app python -c "from app.db.models import Base; from sqlalchemy import create_engine; import os; engine = create_engine(os.environ['DATABASE_URL']); Base.metadata.create_all(engine)"
- Rate limit on embeddings: wait 60s, re-run in batches of 50
