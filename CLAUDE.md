# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A Fusion 360 documentation assistant built with Streamlit, LangChain, ChromaDB, and the Google Gemini API. Users ask questions via the UI; answers are sourced from a Chroma vector store of Fusion 360 PDFs, with fallback to a general LLM.

## Environment setup

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Required environment variables (put in `.env` at project root):
- `GOOGLE_API_KEY` — Google Generative AI key (Gemini)
- `DATABASE_URL` — PostgreSQL connection string (optional; app runs without it, using in-memory session state)

## Running the app

```bash
# Local (no DB)
streamlit run app/main.py

# With PostgreSQL via Docker
docker-compose up --build
```

## Building the vector store

Place Fusion 360 PDF files in `app/rag/data/raw/`, then run:

```bash
cd app/rag
python embeddings.py
```

This chunks PDFs, filters by relevance keywords, embeds with `gemini-embedding-001`, and persists to `app/rag/vectorstore/`.

## Running tests / search diagnostics

```bash
# Verify vectorstore contents
cd app/rag
python test_rag_search.py

# Verify embedding pipeline
python test_embeddings.py
```

There is no pytest suite; the test files are standalone scripts.

## Database migrations (Alembic)

```bash
# Apply migrations (runs automatically on startup when DATABASE_URL is set)
alembic upgrade head

# Generate a new migration after model changes
alembic revision --autogenerate -m "description"
```

## Architecture

Query flow (4 layers):

```
User Question
↓
Router (rule-based intent detection)
↓
Tools (explain_term / recommend_workflow / find_doc_section)
↓ (if no tool match)
RAG (ChromaDB vector search → Gemini answer)
↓ (if answer insufficient)
LLM Fallback (Gemini general knowledge)
```

Source labels returned: `tool:explain_term` | `tool:recommend_workflow` | `tool:find_doc_section` | `rag` | `rag+llm` | `llm_fallback` | `error`

Entry point is `app/rag/assistant.py:answer_question`. Each response dict carries `answer`, `source`, and `usage` (token counts + `cost_usd`).

**Session persistence** (`app/db/`) — SQLAlchemy + PostgreSQL via Alembic. `db/session.py:get_db()` yields `None` gracefully when no DB is configured, falling back to `st.session_state`.

**Advanced RAG utilities** (defined but not yet wired into the main pipeline):
- `app/rag/query_translation.py` — rewrites queries for better retrieval
- `app/rag/compression.py` — compresses retrieved context before generation
- `app/rag/pipeline.py`, `retriever.py` — additional pipeline abstractions

The LLM model is `gemini-2.5-flash` throughout; hardcoded as `MODEL_NAME` in `assistant.py` and `qa.py`.

## Key design decisions

- **ChromaDB local** — no external vector DB cost, persistent via Docker volume
- **Gemini 2.5 Flash** — free tier, replaces OpenAI, handles both embeddings and generation
- **Graceful DB-less mode** — app runs without PostgreSQL (falls back to `st.session_state` history)
- **Alembic migrations** — run automatically on app startup via `main.py`

## What NOT to touch

- `alembic/versions/` — never edit migration files manually
- `app/rag/vectorstore/` — managed by `embeddings.py`, do not delete manually
- `.env` — never commit; contains `GOOGLE_API_KEY` and Postgres credentials

## CI/CD

- GitHub Actions: `.github/workflows/ci.yml`
- Pipeline: Python 3.12 setup → pip install → import check → `docker compose build`
- Docker: two services (`app` + `db`), `postgres_data` named volume
- Deployment target: AWS ECS Fargate (planned)
