from app.retrieval.reranker import rerank_results


# Reason:
# Reranker should always respect top_n limits.
# This is important for token budgeting and retrieval control.
def test_reranker_respects_top_n():
    query = "What is hx-trigger?"

    documents = [
        "doc 1",
        "doc 2",
        "doc 3",
        "doc 4",
    ]

    metadatas = [
        {"source": f"doc{i}.md"}
        for i in range(4)
    ]

    results = rerank_results(
        query=query,
        documents=documents,
        metadatas=metadatas,
        top_n=2,
    )

    assert len(results) == 2


# Reason:
# Reranker output structure should remain stable.
# Downstream pipeline depends on these fields.
def test_reranker_returns_expected_fields():
    query = "What is hx-get?"

    documents = [
        "hx-get performs GET requests"
    ]

    metadatas = [
        {"source": "hx-get.md"}
    ]

    results = rerank_results(
        query=query,
        documents=documents,
        metadatas=metadatas,
    )

    result = results[0]

    assert "document" in result
    assert "metadata" in result
    assert "rerank_score" in result


# Reason:
# Metadata must survive reranking.
# Future citations depend on metadata integrity.
def test_reranker_preserves_metadata():
    query = "What is hx-post?"

    documents = [
        "hx-post sends POST requests"
    ]

    metadatas = [
        {
            "source": "hx-post.md",
            "chunk_index": 3,
        }
    ]

    results = rerank_results(
        query=query,
        documents=documents,
        metadatas=metadatas,
    )

    metadata = results[0]["metadata"]

    assert metadata["source"] == "hx-post.md"
    assert metadata["chunk_index"] == 3


# Reason:
# Reranker scores should be sorted descending.
# Highest relevance should appear first.
def test_reranker_returns_sorted_scores():
    query = "What is hx-trigger?"

    documents = [
        "hx-trigger handles events",
        "random unrelated text",
        "hx-get performs requests",
    ]

    metadatas = [
        {"source": "a.md"},
        {"source": "b.md"},
        {"source": "c.md"},
    ]

    results = rerank_results(
        query=query,
        documents=documents,
        metadatas=metadatas,
    )

    scores = [
        result["rerank_score"]
        for result in results
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )