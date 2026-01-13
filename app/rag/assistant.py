import logging
from dotenv import load_dotenv
import os

from routing.router import route_query
from tools.explain_term import explain_term
from tools.recommend_workflow import recommend_workflow
from tools.find_doc_section import find_doc_section
from rag.qa import answer_with_rag
from utils.token_counter import calculate_cost

from openai import OpenAI

# --- ENV ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- LOGGING ---
logging.basicConfig(
    filename="logs/chat.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

MODEL_NAME = "gpt-4.1-mini"

# --- OpenAI client (LLM fallback) ---
client = OpenAI(api_key=api_key)


def zero_usage():
    return {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "cost_usd": 0.0
    }


def call_gpt_fallback(question: str) -> dict:
    """
    LLM fallback + token usage + cost
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": (
                    "Explain the following Fusion 360 question clearly, "
                    "based on general knowledge:\n\n"
                    f"{question}"
                ),
            }
        ],
        temperature=0,
    )

    usage = response.usage
    cost = calculate_cost(
        model=MODEL_NAME,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens
    )

    return {
        "answer": response.choices[0].message.content,
        "usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "cost_usd": cost
        }
    }


def answer_question(question: str) -> dict:
    logging.info(f"Received question: {question}")

    try:
        route = route_query(question)
        logging.info(f"Routing decision: {route}")

        # ---------- TOOL ROUTES ----------
        if route == "explain_term":
            term = question.replace("what is", "").strip()
            tool_answer = explain_term(term)

            if tool_answer and "No predefined explanation" not in tool_answer:
                return {
                    "answer": tool_answer,
                    "source": "tool:explain_term",
                    "usage": zero_usage()
                }
            else:
                logging.info("Explain_term returned nothing, trying RAG...")

        elif route == "recommend_workflow":
            tool_answer = recommend_workflow("parametric design")
            if tool_answer:
                return {
                    "answer": tool_answer,
                    "source": "tool:recommend_workflow",
                    "usage": zero_usage()
                }
            else:
                logging.info("Recommend_workflow returned nothing, trying RAG...")

        elif route == "find_doc_section":
            tool_answer = find_doc_section(question)
            if tool_answer:
                return {
                    "answer": tool_answer,
                    "source": "tool:find_doc_section",
                    "usage": zero_usage()
                }
            else:
                logging.info("Find_doc_section returned nothing, trying RAG...")

        # ---------- RAG ----------
        rag_result = answer_with_rag(question)

        if rag_result.get("found_docs") is True:
            rag_answer = rag_result.get("answer", "").strip()

            # 🚑 MINŐSÉGI FALLBACK – nem csak found_docs alapján
            if (
                not rag_answer
                or rag_answer.lower().startswith("the provided context does not")
                or rag_answer.lower().startswith("the context does not")
                or len(rag_answer) < 50
            ):
                logging.info("RAG answer insufficient, enriching with LLM fallback")

                fallback = call_gpt_fallback(question)

                return {
                    "answer": (
                        f"{rag_answer}\n\n"
                        "Additional explanation (general knowledge):\n"
                        f"{fallback['answer']}"
                    ),
                    "usage": fallback["usage"],     # 👈 a fallback költségét mutatjuk
                    "source": "rag+llm",
                }

            logging.info("Answered via RAG (sufficient)")
            return {
                "answer": rag_answer,
                "usage": rag_result.get("usage") or zero_usage(),
                "source": "rag",
            }

        # ---------- FALLBACK (NO DOCS) ----------
        logging.info("RAG found no documents, falling back to LLM")
        fallback = call_gpt_fallback(question)
        return {
            "answer": fallback["answer"],
            "usage": fallback["usage"],
            "source": "llm_fallback",
        }

    except Exception:
        logging.exception("Unhandled error in assistant")
        return {
            "answer": "Sorry, there was an internal error.",
            "source": "error",
            "usage": zero_usage()
        }