from types import SimpleNamespace
from unittest.mock import patch

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from app.agent.nodes.evaluate_node import (
    evaluate_node,
)


def _mock_response(content: str):
    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=content
                )
            )
        ]
    )


# Reason:
# PASS should append to history and clear retry reason.
@patch("app.agent.nodes.evaluate_node.client.chat.completions.create")
def test_evaluate_node_pass(
    mock_create,
):
    mock_create.return_value = _mock_response(
        "PASS"
    )

    state = {
        "query": "What is hx-post?",
        "answer": "hx-post does X",
        "citations": [
            {
                "source": "doc.md",
                "chunk_index": 1,
            }
        ],
        "used_rag": True,
        "rewritten_query": "hx-post",
        "loop_count": 0,
        "max_loops": 1,
    }

    result = evaluate_node(state)

    assert result["needs_retry"] is False
    assert result["retry_reason"] == ""

    history = result["chat_history"]
    assert len(history) == 2
    assert isinstance(history[0], HumanMessage)
    assert isinstance(history[1], AIMessage)
    assert history[1].additional_kwargs[
        "citations"
    ] == [
        {
            "source": "doc.md",
            "chunk_index": 1,
        }
    ]


# Reason:
# RETRY should increment loop count and avoid history.
@patch("app.agent.nodes.evaluate_node.client.chat.completions.create")
def test_evaluate_node_retry_once(
    mock_create,
):
    mock_create.return_value = _mock_response(
        "RETRY: not grounded"
    )

    state = {
        "query": "What is hx-post?",
        "answer": "guess",
        "loop_count": 0,
        "max_loops": 1,
        "chat_history": [],
    }

    result = evaluate_node(state)

    assert result["needs_retry"] is True
    assert result["retry_reason"] == "not grounded"
    assert result["loop_count"] == 1
    assert result["chat_history"] == []


# Reason:
# RETRY after max loops should pass and clear reason.
@patch("app.agent.nodes.evaluate_node.client.chat.completions.create")
def test_evaluate_node_retry_exhausted(
    mock_create,
):
    mock_create.return_value = _mock_response(
        "RETRY: still weak"
    )

    state = {
        "query": "What is hx-post?",
        "answer": "guess",
        "loop_count": 1,
        "max_loops": 1,
        "chat_history": [],
    }

    result = evaluate_node(state)

    assert result["needs_retry"] is False
    assert result["retry_reason"] == ""
    assert len(result["chat_history"]) == 2
