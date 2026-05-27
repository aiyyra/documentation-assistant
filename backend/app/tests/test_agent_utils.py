from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from app.agent.utils import format_history


# Reason:
# History formatting should preserve order and roles.
def test_format_history_limits_and_roles():
    history = [
        HumanMessage(content="hi"),
        AIMessage(content="hello"),
        HumanMessage(content="q1"),
        AIMessage(content="a1"),
    ]

    formatted = format_history(
        history,
        max_messages=3,
    )

    lines = formatted.split("\n")

    assert "user: hi" not in formatted
    assert lines[0] == "assistant: hello"
    assert lines[1] == "user: q1"
    assert lines[2] == "assistant: a1"
