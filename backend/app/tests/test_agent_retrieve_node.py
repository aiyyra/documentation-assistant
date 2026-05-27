from unittest.mock import patch

from langchain_core.messages import HumanMessage

from app.agent.nodes.retrieve_node import (
    retrieve_node,
)


# Reason:
# Retrieval node should surface rewritten query and citations.
@patch("app.agent.nodes.retrieve_node.rerank_results")
@patch("app.agent.nodes.retrieve_node.hybrid_retrieve")
@patch("app.agent.nodes.retrieve_node.rewrite_query_with_history")
def test_retrieve_node_with_history(
    mock_rewrite,
    mock_retrieve,
    mock_rerank,
):
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
            "rerank_score": 1.2,
        }
    ]

    state = {
        "query": "What is hx-post?",
        "chat_history": [
            HumanMessage(content="Hi")
        ],
    }

    result = retrieve_node(state)

    assert result["used_rag"] is True
    assert result["route"] == "rag"
    assert result["rewritten_query"] == "rewritten"
    assert result["retrieved_chunks"] == [
        "chunk a"
    ]
    assert result["citations"] == [
        {
            "source": "doc.md",
            "chunk_index": 1,
        }
    ]


# Reason:
# Retry reason should be included in rewrite input.
@patch("app.agent.nodes.retrieve_node.rewrite_query")
@patch("app.agent.nodes.retrieve_node.hybrid_retrieve")
@patch("app.agent.nodes.retrieve_node.rerank_results")
def test_retrieve_node_retry_reason(
    mock_rerank,
    mock_retrieve,
    mock_rewrite,
):
    mock_rewrite.return_value = "rewritten"
    mock_retrieve.return_value = []
    mock_rerank.return_value = []

    state = {
        "query": "Explain hx-post",
        "retry_reason": "missing usage details",
    }

    retrieve_node(state)

    mock_rewrite.assert_called_once()
    called_arg = mock_rewrite.call_args[0][0]
    assert "missing usage details" in called_arg
