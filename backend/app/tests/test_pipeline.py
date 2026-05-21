from unittest.mock import patch

from app.rag.pipeline import ask


# Reason:
# We do not want tests depending on real OpenAI API calls.
# External APIs make tests slow, expensive, and unstable.
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.retrieve")
def test_pipeline_returns_expected_structure(
    mock_retrieve,
    mock_generate,
):
    mock_retrieve.return_value = {
        "documents": [["sample chunk"]],
        "metadatas": [[
            {
                "source": "doc.md",
                "chunk_index": 0,
            }
        ]],
    }

    mock_generate.return_value = "sample answer"

    result = ask("What is hx-trigger?")

    assert "answer" in result
    assert "documents" in result
    assert "metadata" in result


# Reason:
# Pipeline orchestration should pass retrieved chunks into generation.
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.retrieve")
def test_pipeline_returns_generated_answer(
    mock_retrieve,
    mock_generate,
):
    mock_retrieve.return_value = {
        "documents": [["sample chunk"]],
        "metadatas": [[
            {
                "source": "doc.md",
                "chunk_index": 0,
            }
        ]],
    }

    mock_generate.return_value = "This is the generated answer"

    result = ask("test")

    assert result["answer"] == "This is the generated answer"


# Reason:
# Metadata propagation is important for future citation systems.
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.retrieve")
def test_pipeline_preserves_metadata(
    mock_retrieve,
    mock_generate,
):
    mock_retrieve.return_value = {
        "documents": [["sample chunk"]],
        "metadatas": [[
            {
                "source": "hx-trigger.md",
                "chunk_index": 3,
            }
        ]],
    }

    mock_generate.return_value = "answer"

    result = ask("test")

    metadata = result["metadata"][0]

    assert metadata["source"] == "hx-trigger.md"
    assert metadata["chunk_index"] == 3