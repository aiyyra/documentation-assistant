from app.ingestion.chunker import chunk_document


# Reason:
# Chunking is a core RAG behavior.
# We need confidence that large documents are actually split.
def test_chunk_document_splits_large_text():
    text = "A" * 5000

    chunks = chunk_document(text)

    assert len(chunks) > 1


# Reason:
# Empty inputs should not produce invalid chunks.
def test_chunk_document_handles_empty_text():
    chunks = chunk_document("")

    assert chunks == []


# Reason:
# We want to ensure chunker returns strings only.
def test_chunk_document_returns_strings():
    text = "Hello world " * 100

    chunks = chunk_document(text)

    assert all(isinstance(chunk, str) for chunk in chunks)