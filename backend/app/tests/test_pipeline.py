from unittest.mock import patch

from app.rag.pipeline import ask


# Reason:
# We do not want tests depending on real OpenAI API calls.
# External APIs make tests slow, expensive, and unstable.
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.hybrid_retrieve")
@patch("app.rag.pipeline.rewrite_query")
def test_pipeline_returns_expected_structure(
    mock_rewrite,
    mock_retrieve,
    mock_generate,
):
    mock_rewrite.return_value = (
        "htmx hx-trigger events"
    )

    mock_retrieve.return_value = [
        {
            "document": "sample chunk",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 0,
            },
            "retrieval_source": "vector",
        }
    ]

    mock_generate.return_value = "sample answer"

    result = ask("What is hx-trigger?")

    assert "original_query" in result
    assert "rewritten_query" in result

    assert "answer" in result
    assert "documents" in result
    assert "metadata" in result

    assert "retrieval_results" in result
    assert "reranked_results" in result


# Reason:
# Pipeline orchestration should preserve generated responses.
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.hybrid_retrieve")
@patch("app.rag.pipeline.rewrite_query")
def test_pipeline_returns_generated_answer(
    mock_rewrite,
    mock_retrieve,
    mock_generate,
):
    mock_rewrite.return_value = (
        "htmx hx-get requests"
    )

    mock_retrieve.return_value = [
        {
            "document": "sample chunk",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 0,
            },
            "retrieval_source": "vector",
        }
    ]

    mock_generate.return_value = (
        "This is the generated answer"
    )

    result = ask("test")

    assert (
        result["answer"]
        ==
        "This is the generated answer"
    )


# Reason:
# Metadata propagation is important for citations,
# debugging, and retrieval observability.
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.hybrid_retrieve")
@patch("app.rag.pipeline.rewrite_query")
def test_pipeline_preserves_metadata(
    mock_rewrite,
    mock_retrieve,
    mock_generate,
):
    mock_rewrite.return_value = (
        "htmx hx-trigger"
    )

    mock_retrieve.return_value = [
        {
            "document": "sample chunk",
            "metadata": {
                "source": "hx-trigger.md",
                "chunk_index": 3,
            },
            "retrieval_source": "bm25",
        }
    ]

    mock_generate.return_value = "answer"

    result = ask("test")

    metadata = result["metadata"][0]

    assert (
        metadata["source"]
        ==
        "hx-trigger.md"
    )

    assert (
        metadata["chunk_index"]
        ==
        3
    )


# Reason:
# Retrieval should use rewritten queries,
# not raw user queries.
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.hybrid_retrieve")
@patch("app.rag.pipeline.rewrite_query")
def test_pipeline_uses_rewritten_query_for_retrieval(
    mock_rewrite,
    mock_retrieve,
    mock_generate,
):
    mock_rewrite.return_value = (
        "htmx hx-trigger events"
    )

    mock_retrieve.return_value = [
        {
            "document": "sample chunk",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 0,
            },
            "retrieval_source": "vector",
        }
    ]

    mock_generate.return_value = "answer"

    ask("How do I trigger requests?")

    mock_retrieve.assert_called_with(
        query="htmx hx-trigger events",
        vector_top_k=10,
        bm25_top_k=10,
    )


# Reason:
# Original and rewritten queries should both remain
# accessible for debugging and observability.
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.hybrid_retrieve")
@patch("app.rag.pipeline.rewrite_query")
def test_pipeline_preserves_original_and_rewritten_query(
    mock_rewrite,
    mock_retrieve,
    mock_generate,
):
    mock_rewrite.return_value = (
        "htmx partial page updates"
    )

    mock_retrieve.return_value = [
        {
            "document": "sample chunk",
            "metadata": {
                "source": "doc.md",
                "chunk_index": 0,
            },
            "retrieval_source": "vector",
        }
    ]

    mock_generate.return_value = "answer"

    result = ask(
        "How do I update part of the page?"
    )

    assert (
        result["original_query"]
        ==
        "How do I update part of the page?"
    )

    assert (
        result["rewritten_query"]
        ==
        "htmx partial page updates"
    )