from types import SimpleNamespace
from unittest.mock import patch

from app.agent.router import (
    route_query,
    route_query_with_history,
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
# Router should normalize valid responses.
@patch("app.agent.router.client.chat.completions.create")
def test_route_query_normalizes_output(mock_create):
    mock_create.return_value = _mock_response("RAG")

    result = route_query("What is hx-post?")

    assert result == "rag"


# Reason:
# Invalid router output should default to rag.
@patch("app.agent.router.client.chat.completions.create")
def test_route_query_defaults_to_rag(mock_create):
    mock_create.return_value = _mock_response("other")

    result = route_query("Unknown")

    assert result == "rag"


# Reason:
# History-aware routing should run without error.
@patch("app.agent.router.client.chat.completions.create")
def test_route_query_with_history(mock_create):
    mock_create.return_value = _mock_response(
        "conversational"
    )

    result = route_query_with_history(
        "Thanks",
        [],
    )

    assert result == "conversational"
