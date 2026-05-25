import os
import sys
from pathlib import Path

import streamlit as st


# Allow importing backend modules without modifying backend code.
REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = REPO_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from app.rag.pipeline import ask  # noqa: E402


st.set_page_config(
    page_title="HTMX RAG Assistant",
    page_icon="\U0001F4D6",
    layout="wide",
)

st.title("HTMX RAG Assistant")
st.caption("Agentic RAG demo (chat-style UI)")

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_message(message: dict) -> None:
    role = message.get("role", "assistant")
    content = message.get("content", "")
    citations = message.get("citations", [])

    with st.chat_message(role):
        st.markdown(content)

        if citations:
            with st.expander("Citations", expanded=False):
                for citation in citations:
                    source = citation.get("source", "unknown")
                    chunk = citation.get("chunk_index", "?")
                    st.write(f"- {source} (chunk {chunk})")


for msg in st.session_state.messages:
    render_message(msg)

prompt = st.chat_input("Ask about HTMX docs")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = ask(prompt)
                answer = result.get("answer", "No answer returned.")
                citations = result.get("citations", [])

                st.markdown(answer)

                if citations:
                    with st.expander("Citations", expanded=False):
                        for citation in citations:
                            source = citation.get("source", "unknown")
                            chunk = citation.get("chunk_index", "?")
                            st.write(f"- {source} (chunk {chunk})")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "citations": citations,
                    }
                )
            except Exception as exc:
                error_message = (
                    "Error while generating a response. "
                    "Check that the backend .venv is active and "
                    "OPENAI_API_KEY is set."
                )
                st.error(error_message)
                st.exception(exc)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )
