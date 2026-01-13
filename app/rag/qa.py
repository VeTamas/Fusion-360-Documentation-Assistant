from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from utils.token_counter import calculate_cost

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

MODEL_NAME = "gpt-4.1-mini"


def answer_with_rag(question: str) -> dict:
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(
        persist_directory=str(VECTORSTORE_DIR),
        embedding_function=embeddings
    )

    docs = vectordb.similarity_search(question, k=5)

    if not docs:
        return {"found_docs": False, "answer": "", "usage": None}

    context = "\n\n".join(d.page_content for d in docs)

    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

    prompt = f"""
You are a Fusion 360 documentation assistant.

Use ONLY the context below to answer the question.
If the answer is not explicitly contained in the context, say so.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    answer_text = response.content.strip() if response.content else ""

    meta = response.response_metadata or {}
    prompt_tokens = meta.get("prompt_tokens", 0)
    completion_tokens = meta.get("completion_tokens", 0)
    total_tokens = meta.get("total_tokens", 0)

    cost = calculate_cost(
        model=MODEL_NAME,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens
    )

    return {
        "found_docs": True,
        "answer": answer_text,
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost
        }
    }