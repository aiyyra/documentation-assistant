from app.retrieval.bm25_retriever import (
    retrieve_bm25,
)


# Reason:
# BM25 retriever should respect top_k limits.
# Retrieval size control matters for downstream reranking.
def test_bm25_respects_top_k():
    results = retrieve_bm25(
        query="hx-trigger",
        top_k=3,
    )

    assert len(results) == 3


# Reason:
# Retrieval output structure must remain stable.
# Downstream hybrid retrieval depends on these fields.
def test_bm25_returns_expected_fields():
    results = retrieve_bm25(
        query="hx-get",
        top_k=1,
    )

    result = results[0]

    assert "document" in result
    assert "metadata" in result
    assert "bm25_score" in result


# Reason:
# Metadata integrity is important for citations and debugging.
def test_bm25_preserves_metadata():
    results = retrieve_bm25(
        query="hx-post",
        top_k=1,
    )

    metadata = results[0]["metadata"]

    assert "source" in metadata
    assert "chunk_index" in metadata


# Reason:
# BM25 scores should be sorted descending.
# Most relevant chunks should appear first.
def test_bm25_returns_sorted_scores():
    results = retrieve_bm25(
        query="hx-trigger",
        top_k=5,
    )

    scores = [
        result["bm25_score"]
        for result in results
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


# Reason:
# BM25 should successfully retrieve technical keywords.
# Exact keyword matching is one of BM25's main strengths.
def test_bm25_retrieves_technical_terms():
    results = retrieve_bm25(
        query="hx-swap-oob",
        top_k=5,
    )

    documents = [
        result["document"]
        for result in results
    ]

    combined_text = " ".join(documents).lower()

    assert "hx-swap-oob" in combined_text