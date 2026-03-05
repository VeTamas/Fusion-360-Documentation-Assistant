# Fusion 360 Documentation Assistant

AI assistant for Autodesk Fusion 360 documentation using Retrieval-Augmented Generation.

The system prioritizes tool-based answers and documentation retrieval before using LLM reasoning to reduce hallucinations.

---

## System flow:

User Question
     │
Tool Router
     │
Documentation Retrieval
     │
LLM Fallback
     │
Answer + Source

## Features

- Advanced RAG using a **Chroma vector database**
- Domain-specific document ingestion and semantic chunking
- **Controlled tool calling** with explicit query routing
- Multi-stage fallback logic (Tool → RAG → LLM)
- Token usage and **estimated cost tracking**
- Logging and error handling for observability
- Modular, extensible architecture

---

## Architecture Overview

1. User queries are received via a Streamlit-based UI
2. A rule-based router determines the intent of the query
3. Depending on the intent, the system:
   - Explains a predefined term
   - Recommends a workflow
   - Finds relevant documentation sections
   - Falls back to RAG-based answering
4. The RAG pipeline retrieves relevant Fusion 360 documentation chunks
   from a Chroma vector store
5. A ChatGPT-based model generates a grounded response
6. If the RAG answer is insufficient, the system falls back to a general LLM
   while clearly labeling the response source

Each response includes metadata indicating:
- the answering strategy (`tool`, `rag`, `rag+llm`, `llm_fallback`)
- token usage and estimated cost (where applicable)

---

## Tech Stack

- Python
- LangChain
- OpenAI API
- ChromaDB
- Streamlit

---

## Project Structure

```text
app/            # Streamlit UI
tools/          # Deterministic tools (term explanation, workflows, etc.)
routing/        # Query routing logic
utils/          # Token and cost calculation utilities
data/           # Raw documentation files
vectorstore/    # Persisted Chroma vector database
logs/           # Application logs
```

---

## Setup

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

Set your OpenAI API key:
export OPENAI_API_KEY=your_key_here
# Windows:
setx OPENAI_API_KEY your_key_here

---

## Running the application

streamlit run app/main.py

---

## Token Usage & Cost Tracking

Token usage and estimated cost are tracked for:
-RAG-based answers (when metadata is available)
-LLM fallback answers (via OpenAI SDK usage data)
-Tool-based answers do not incur token usage and are explicitly reported as zero-cost
-Cost estimates are displayed in the UI per response

---

## Notes

-The system prioritizes documentation-grounded answers
-Fallback to a general LLM is used only when documentation coverage is insufficient
-The architecture is designed to be extensible for:
   - advanced retrieval strategies
   - automated knowledge base updates
   - multi-user or cloud deployment scenarios
