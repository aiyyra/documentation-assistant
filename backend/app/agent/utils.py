from langchain_core.messages import BaseMessage


def format_history(
    chat_history: list[BaseMessage] | None,
    max_messages: int = 6,
) -> str:
    if not chat_history:
        return ""

    recent = chat_history[-max_messages:]
    formatted_lines = []

    for message in recent:
        role = (
            "user"
            if message.type == "human"
            else "assistant"
        )
        formatted_lines.append(
            f"{role}: {message.content}"
        )

    return "\n".join(formatted_lines)
