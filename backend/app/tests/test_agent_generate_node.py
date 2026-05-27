from unittest.mock import patch

from langchain_core.messages import HumanMessage

from app.agent.nodes.generate_node import (
    generate_node,
)


# Reason:
# Generator should return an answer and keep history intact.
@patch("app.agent.nodes.generate_node.generate_response")
def test_generate_node_returns_answer(
    mock_generate,
):
    mock_generate.return_value = "ok"

    chat_history = [
        HumanMessage(content="hi")
    ]

    state = {
        "query": "What is hx-post?",
        "chat_history": chat_history,
        "context_block": "chunk",
        "route": "rag",
    }

    result = generate_node(state)

    assert result["answer"] == "ok"
    assert result["route"] == "rag"
    assert result["chat_history"] is chat_history
