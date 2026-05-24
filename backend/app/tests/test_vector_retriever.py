from app.retrieval.vector_retriever import retrieve


# Reason:
# Retrieval is the core intelligence layer.
# We verify the retrieval pipeline returns expected structure.
def test_retrieve_returns_results():
    results = retrieve("What is hx-trigger?", top_k=3)

    assert "documents" in results
    assert "metadatas" in results
    assert len(results["documents"][0]) > 0


# Reason:
# top_k behavior is important for retrieval tuning.
def test_retrieve_respects_top_k():
    results = retrieve("What is hx-get?", top_k=2)

    assert len(results["documents"][0]) == 2


# Reason:
# Retrieved chunks should include metadata for future citations.
def test_retrieve_returns_metadata():
    results = retrieve("What is hx-post?", top_k=1)

    metadata = results["metadatas"][0][0]

    assert "source" in metadata
    assert "chunk_index" in metadata