from app.retrieval.hybrid_retriever import (
    hybrid_retrieve,
)


# Reason:
# Hybrid retrieval should return usable results.
def test_hybrid_returns_results():
    results = hybrid_retrieve(
        query="hx-trigger",
    )

    assert len(results) > 0


# Reason:
# Retrieval source metadata is important for debugging
# and future retrieval observability.
def test_hybrid_results_include_source_type():
    results = hybrid_retrieve(
        query="hx-get",
    )

    result = results[0]

    assert "retrieval_source" in result


# Reason:
# Duplicate chunks waste reranking capacity and token budget.
# Hybrid retrieval should deduplicate results.
def test_hybrid_results_are_deduplicated():
    results = hybrid_retrieve(
        query="hx-post",
    )

    documents = [
        result["document"]
        for result in results
    ]

    assert len(documents) == len(set(documents))


# Reason:
# Metadata integrity must survive retrieval fusion.
def test_hybrid_preserves_metadata():
    results = hybrid_retrieve(
        query="hx-swap",
    )

    metadata = results[0]["metadata"]

    assert "source" in metadata
    assert "chunk_index" in metadata