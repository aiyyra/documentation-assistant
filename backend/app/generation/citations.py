def build_citations(
    metadatas: list[dict],
):
    seen = set()

    citations = []

    for metadata in metadatas:
        citation_key = (
            metadata["source"],
            metadata["chunk_index"],
        )

        if citation_key not in seen:
            citations.append(
                {
                    "source": metadata["source"],
                    "chunk_index": metadata["chunk_index"],
                }
            )

            seen.add(citation_key)

    return citations