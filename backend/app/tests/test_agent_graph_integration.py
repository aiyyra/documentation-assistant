from types import SimpleNamespace
from unittest.mock import patch

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from app.agent.graph import graph


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


@patch("app.agent.graph.route_query_with_history")
@patch("app.agent.nodes.generate_node.generate_response")
@patch("app.agent.nodes.evaluate_node.client.chat.completions.create")
@patch("app.agent.graph.retrieve_node")
def test_graph_conversational_path(
    mock_retrieve,
    mock_eval,
    mock_generate,
    mock_route,
):
    mock_route.return_value = "conversational"
    mock_generate.return_value = "ok"
    mock_eval.return_value = _mock_response("PASS")

    result = graph.invoke(
        {
            "query": "hi",
            "chat_history": [],
            "loop_count": 0,
            "max_loops": 1,
        }
    )

    assert result["answer"] == "ok"
    assert result["route"] == "conversational"
    assert len(result["chat_history"]) == 2
    assert isinstance(result["chat_history"][0], HumanMessage)
    assert isinstance(result["chat_history"][1], AIMessage)
    mock_retrieve.assert_not_called()


@patch("app.agent.graph.route_query_with_history")
@patch("app.agent.nodes.retrieve_node.rewrite_query")
@patch("app.agent.nodes.retrieve_node.hybrid_retrieve")
@patch("app.agent.nodes.retrieve_node.rerank_results")
@patch("app.agent.nodes.generate_node.generate_response")
@patch("app.agent.nodes.evaluate_node.client.chat.completions.create")
def test_graph_rag_path(
    mock_eval,
    mock_generate,
    mock_rerank,
    mock_retrieve,
    mock_rewrite,
    mock_route,
):
    mock_route.return_value = "rag"
    mock_eval.return_value = _mock_response("PASS")
    mock_generate.return_value = "ok"
    mock_rewrite.return_value = "rewritten"

    mock_retrieve.return_value = [
        {
            "document": "chunk a",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 1,
            },
        }
    ]

    mock_rerank.return_value = [
        {
            "document": "chunk a",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 1,
            },
            "rerank_score": 1.0,
        }
    ]

    result = graph.invoke(
        {
            "query": "What is hx-post?",
            "chat_history": [],
            "loop_count": 0,
            "max_loops": 1,
        }
    )

    assert result["used_rag"] is True
    assert result["context_block"] == "chunk a"
    assert result["citations"] == [
        {
            "source": "doc.md",
            "chunk_index": 1,
        }
    ]
    assert result["answer"] == "ok"


@patch("app.agent.graph.route_query_with_history")
@patch("app.agent.nodes.retrieve_node.rewrite_query")
@patch("app.agent.nodes.retrieve_node.hybrid_retrieve")
@patch("app.agent.nodes.retrieve_node.rerank_results")
@patch("app.agent.nodes.generate_node.generate_response")
@patch("app.agent.nodes.evaluate_node.client.chat.completions.create")
def test_graph_retry_loop_once(
    mock_eval,
    mock_generate,
    mock_rerank,
    mock_retrieve,
    mock_rewrite,
    mock_route,
):
    mock_route.return_value = "rag"
    mock_eval.side_effect = [
        _mock_response("RETRY: not grounded"),
        _mock_response("PASS"),
    ]
    mock_generate.return_value = "ok"
    mock_rewrite.return_value = "rewritten"

    mock_retrieve.return_value = [
        {
            "document": "chunk a",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 1,
            },
        }
    ]

    mock_rerank.return_value = [
        {
            "document": "chunk a",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 1,
            },
            "rerank_score": 1.0,
        }
    ]

    result = graph.invoke(
        {
            "query": "What is hx-post?",
            "chat_history": [],
            "loop_count": 0,
            "max_loops": 1,
        }
    )

    assert result["loop_count"] == 1
    assert result["needs_retry"] is False
    assert mock_retrieve.call_count == 2


@patch("app.agent.graph.route_query_with_history")
@patch("app.agent.nodes.retrieve_node.rewrite_query")
@patch("app.agent.nodes.retrieve_node.hybrid_retrieve")
@patch("app.agent.nodes.retrieve_node.rerank_results")
@patch("app.agent.nodes.generate_node.generate_response")
@patch("app.agent.nodes.evaluate_node.client.chat.completions.create")
def test_graph_history_metadata_no_chunk_leak(
    mock_eval,
    mock_generate,
    mock_rerank,
    mock_retrieve,
    mock_rewrite,
    mock_route,
):
    mock_route.return_value = "rag"
    mock_eval.return_value = _mock_response("PASS")
    mock_generate.return_value = "ok"
    mock_rewrite.return_value = "rewritten"

    mock_retrieve.return_value = [
        {
            "document": "chunk a",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 1,
            },
        }
    ]

    mock_rerank.return_value = [
        {
            "document": "chunk a",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 1,
            },
            "rerank_score": 1.0,
        }
    ]

    result = graph.invoke(
        {
            "query": "What is hx-post?",
            "chat_history": [],
            "loop_count": 0,
            "max_loops": 1,
        }
    )

    history = result["chat_history"]
    last_message = history[-1]

    assert "chunk a" not in last_message.content
    assert last_message.additional_kwargs[
        "citations"
    ] == [
        {
            "source": "doc.md",
            "chunk_index": 1,
        }
    ]
