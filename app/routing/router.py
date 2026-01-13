def route_query(question: str) -> str:
    q = question.lower()

    if any(k in q for k in ["what is", "define", "meaning of"]):
        return "explain_term"

    if any(k in q for k in ["how do i", "steps", "workflow"]):
        return "recommend_workflow"

    if any(k in q for k in ["where", "which section", "documentation"]):
        return "find_doc_section"

    return "rag"