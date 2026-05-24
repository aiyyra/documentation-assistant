from app.retrieval.vector_retriever import retrieve_vector


# Reason:
# Retrieval is the core intelligence layer.
# We verify the retrieval pipeline returns expected structure.
def test_retrieve_returns_results():
    results = retrieve_vector("What is hx-trigger?", top_k=3)

    assert isinstance(results, list)
    assert len(results) > 0

    first = results[0]

    assert "document" in first
    assert "metadata" in first
    assert "vector_score" in first
    assert "retrieval_source" in first


# Reason:
# top_k behavior is important for retrieval tuning.
def test_retrieve_respects_top_k():
    results = retrieve_vector("What is hx-get?", top_k=2)

    assert len(results) == 2


# Reason:
# Retrieved chunks should include metadata for future citations.
def test_retrieve_returns_metadata():
    results = retrieve_vector("What is hx-post?", top_k=1)

    metadata = results[0]["metadata"]

    assert "source" in metadata
    assert "chunk_index" in metadata