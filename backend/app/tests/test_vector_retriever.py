from pathlib import Path

import pytest

from app.retrieval.vector_retriever import retrieve_vector


CHUNK_PATH = Path(
    "data/processed/chunks/htmx_chunks.json"
)


@pytest.mark.integration
@pytest.mark.skipif(
    not CHUNK_PATH.exists(),
    reason="chunks not indexed",
)
def test_retrieve_returns_results():
    results = retrieve_vector("What is hx-trigger?", top_k=3)

    assert isinstance(results, list)
    assert len(results) > 0

    first = results[0]

    assert "document" in first
    assert "metadata" in first
    assert "vector_score" in first
    assert "retrieval_source" in first


@pytest.mark.integration
@pytest.mark.skipif(
    not CHUNK_PATH.exists(),
    reason="chunks not indexed",
)
def test_retrieve_respects_top_k():
    results = retrieve_vector("What is hx-get?", top_k=2)

    assert len(results) == 2


@pytest.mark.integration
@pytest.mark.skipif(
    not CHUNK_PATH.exists(),
    reason="chunks not indexed",
)
def test_retrieve_returns_metadata():
    results = retrieve_vector("What is hx-post?", top_k=1)

    metadata = results[0]["metadata"]

    assert "source" in metadata
    assert "chunk_index" in metadata