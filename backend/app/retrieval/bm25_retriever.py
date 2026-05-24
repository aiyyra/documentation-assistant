from app.retrieval.bm25_indexer import (
    bm25,
    chunks,
)
from app.retrieval.tokenizer import tokenize


def retrieve_bm25(
    query: str,
    top_k: int = 10,
):
    tokenized_query = tokenize(query)

    scores = bm25.get_scores(tokenized_query)

    scored_chunks = []

    for chunk, score in zip(chunks, scores):
        scored_chunks.append(
            {
                "document": chunk["text"],
                "metadata": {
                    "source": chunk["source"],
                    "chunk_index": chunk["chunk_index"],
                },
                "bm25_score": float(score),
                "retrieval_source": "bm25",
            }
        )

    scored_chunks.sort(
        key=lambda x: x["bm25_score"],
        reverse=True,
    )

    return scored_chunks[:top_k]


if __name__ == "__main__":
    while True:
        query = input("\nBM25 Query > ")

        if query.lower() in ["exit", "quit"]:
            break

        results = retrieve_bm25(query)

        for idx, result in enumerate(results, start=1):
            print("=" * 80)

            print(f"[RESULT {idx}]")
            print(f"Score: {result['bm25_score']:.4f}")

            metadata = result["metadata"]

            print(
                f"Source: {metadata['source']}"
            )

            print(
                f"Chunk: {metadata['chunk_index']}"
            )

            print("\nTEXT:\n")

            print(result["document"][:1000])