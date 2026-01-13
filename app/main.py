import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.assistant import answer_question

st.set_page_config(
    page_title="Fusion 360 Documentation Assistant",
    layout="wide"
)

st.title("Fusion 360 Documentation Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("Ask a question about Fusion 360:")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        result = answer_question(question)

    st.session_state.history.append({
        "question": question,
        "answer": result.get("answer", ""),
        "source": result.get("source", "unknown"),
        "usage": result.get("usage"),
    })

for chat in reversed(st.session_state.history):
    st.markdown(f"**Q:** {chat['question']}")
    st.markdown(f"**A:** {chat['answer']}")
    st.markdown(f"*Source:* `{chat['source']}`")

    usage = chat.get("usage") or {
        "total_tokens": 0,
        "cost_usd": 0.0
    }

    st.markdown(
        f"*Tokens:* {usage.get('total_tokens', 0)} | "
        f"*Estimated cost:* ${usage.get('cost_usd', 0.0):.6f}"
    )

    st.markdown("---")