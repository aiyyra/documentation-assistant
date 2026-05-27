from pathlib import Path

import pytest

from app.retrieval.hybrid_retriever import (
    hybrid_retrieve,
)


CHUNK_PATH = Path(
    "data/processed/chunks/htmx_chunks.json"
)


@pytest.mark.integration
@pytest.mark.skipif(
    not CHUNK_PATH.exists(),
    reason="chunks not indexed",
)
def test_hybrid_returns_results():
    results = hybrid_retrieve(
        query="hx-trigger",
    )

    assert len(results) > 0


@pytest.mark.integration
@pytest.mark.skipif(
    not CHUNK_PATH.exists(),
    reason="chunks not indexed",
)
def test_hybrid_results_include_source_type():
    results = hybrid_retrieve(
        query="hx-get",
    )

    result = results[0]

    assert "retrieval_source" in result


@pytest.mark.integration
@pytest.mark.skipif(
    not CHUNK_PATH.exists(),
    reason="chunks not indexed",
)
def test_hybrid_results_are_deduplicated():
    results = hybrid_retrieve(
        query="hx-post",
    )

    documents = [
        result["document"]
        for result in results
    ]

    assert len(documents) == len(set(documents))


@pytest.mark.integration
@pytest.mark.skipif(
    not CHUNK_PATH.exists(),
    reason="chunks not indexed",
)
def test_hybrid_preserves_metadata():
    results = hybrid_retrieve(
        query="hx-swap",
    )

    metadata = results[0]["metadata"]

    assert "source" in metadata
    assert "chunk_index" in metadata