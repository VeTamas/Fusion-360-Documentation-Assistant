from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

QUERY_TRANSLATION_PROMPT = PromptTemplate.from_template(
    """
You are an expert assistant specialized in Autodesk Fusion 360 documentation.

Rewrite the user's question to be:
- precise
- technical
- optimized for documentation retrieval

User question:
{question}

Rewritten query:
"""
)

def translate_query(question: str) -> str:
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    chain = QUERY_TRANSLATION_PROMPT | llm
    rewritten = chain.invoke({"question": question})

    return rewritten.content.strip()