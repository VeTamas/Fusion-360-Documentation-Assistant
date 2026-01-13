from rag.assistant import answer_question

questions = [
    "What is parametric design?",
    "How do I create a parametric model?",
    "Where can I find this in the documentation?",
    "Explain parametric design in Fusion 360"
]

for q in questions:
    print("\nQ:", q)
    print("A:", answer_question(q))