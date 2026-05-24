from app.retrieval.vector_retriever import (
    retrieve_vector,
)

from app.retrieval.bm25_retriever import (
    retrieve_bm25,
)


def hybrid_retrieve(
    query: str,
    vector_top_k: int = 10,
    bm25_top_k: int = 10,
):
    vector_results = retrieve_vector(
        query=query,
        top_k=vector_top_k,
    )

    bm25_results = retrieve_bm25(
        query=query,
        top_k=bm25_top_k,
    )

    combined_results = (
        vector_results + bm25_results
    )

    deduplicated_results = []

    seen_documents = set()

    for result in combined_results:
        document = result["document"]

        if document not in seen_documents:
            deduplicated_results.append(result)

            seen_documents.add(document)

    return deduplicated_results


if __name__ == "__main__":
    while True:
        query = input("\nHybrid Query > ")

        if query.lower() in ["exit", "quit"]:
            break

        results = hybrid_retrieve(query)

        for idx, result in enumerate(
            results,
            start=1,
        ):
            print("=" * 80)

            print(f"[RESULT {idx}]")

            print(
                f"Source Type: "
                f"{result['retrieval_source']}"
            )

            metadata = result["metadata"]

            print(
                f"Document Source: "
                f"{metadata['source']}"
            )

            print(
                f"Chunk Index: "
                f"{metadata['chunk_index']}"
            )

            if "vector_score" in result:
                print(
                    f"Vector Score: "
                    f"{result['vector_score']:.4f}"
                )

            if "bm25_score" in result:
                print(
                    f"BM25 Score: "
                    f"{result['bm25_score']:.4f}"
                )

            print("\nTEXT:\n")

            print(result["document"][:1000])