from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

COMPRESSION_PROMPT = PromptTemplate.from_template(
    """
You are summarizing Fusion 360 documentation excerpts.

Your goal:
- keep only information relevant to the user's question
- remove redundancy
- preserve technical accuracy

User question:
{question}

Context:
{context}

Compressed context:
"""
)

def compress_context(question: str, docs: list) -> str:
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    context_text = "\n\n".join([doc.page_content for doc in docs])

    chain = COMPRESSION_PROMPT | llm
    compressed = chain.invoke(
        {
            "question": question,
            "context": context_text
        }
    )

    return compressed.content.strip()