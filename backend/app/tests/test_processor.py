from app.ingestion.schemas import Chunk


# Reason:
# Metadata integrity is important for citations and retrieval.
# Broken metadata later causes citation failures.
def test_chunk_schema_to_dict():
    chunk = Chunk(
        id="test_1",
        text="hello",
        source="doc.md",
        chunk_index=0,
    )

    result = chunk.to_dict()

    assert result["id"] == "test_1"
    assert result["source"] == "doc.md"
    assert result["chunk_index"] == 0


# Reason:
# Chunk IDs should remain deterministic and stable.
def test_chunk_id_format():
    chunk = Chunk(
        id="attributes_hx-get_0",
        text="sample",
        source="attributes_hx-get.md",
        chunk_index=0,
    )

    assert "_" in chunk.id