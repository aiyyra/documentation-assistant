from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)


def append_user_message(
    chat_history,
    query: str,
):
    if chat_history is None:
        chat_history = []

    chat_history.append(
        HumanMessage(content=query)
    )

    return chat_history


def append_ai_message(
    chat_history,
    answer: str,
    metadata: dict | None = None,
):
    if chat_history is None:
        chat_history = []

    additional_kwargs = metadata or {}

    chat_history.append(
        AIMessage(
            content=answer,
            additional_kwargs=additional_kwargs,
        )
    )

    return chat_history