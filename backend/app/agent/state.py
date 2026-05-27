from langchain_core.messages import (
    BaseMessage,
)

from typing import TypedDict


class AgentState(TypedDict, total=False):
    query: str

    rewritten_query: str

    route: str

    answer: str

    citations: list

    used_rag: bool

    retrieved_chunks: list[str]

    context_block: str

    retrieval_results: list

    reranked_results: list

    chat_history: list[BaseMessage]