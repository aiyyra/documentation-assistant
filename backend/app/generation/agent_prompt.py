from langchain_core.messages import BaseMessage

from app.agent.utils import format_history


SYSTEM_PROMPT = """
You are an HTMX documentation assistant.

Be concise, clear, and consistent.

If context is provided, answer using it.
If context is not provided, answer conversationally.

If the answer is not contained in the provided context,
say you do not know.
"""


def build_context_block(chunks: list[str]) -> str:
    return "\n\n".join(chunks)


def build_agent_prompt(
    query: str,
    chat_history: list[BaseMessage] | None,
    context_block: str | None,
) -> str:
    history_text = format_history(chat_history)

    context_section = (
        f"\n\nCONTEXT\n\n{context_block}\n"
        if context_block
        else ""
    )

    history_section = (
        f"\n\nCONVERSATION\n\n{history_text}\n"
        if history_text
        else ""
    )

    prompt = (
        f"{SYSTEM_PROMPT}"
        f"{history_section}"
        f"{context_section}"
        f"\n\nQUESTION\n\n{query}\n\nANSWER\n"
    )

    return prompt
