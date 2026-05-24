from app.retrieval.embedder import embed_text
from app.retrieval.vectordb import collection


def retrieve_vector(
    query: str,
    top_k: int = 10,
):
    query_embedding = embed_text([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    formatted_results = []

    for doc, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        formatted_results.append(
            {
                "document": doc,
                "metadata": metadata,
                "vector_score": float(distance),
                "retrieval_source": "vector",
            }
        )

    return formatted_results

def pretty_print(results):
    for idx, result in enumerate(results, start=1):
        print("=" * 80)

        print(f"[RESULT {idx}]")
        print(f"Source: {result['metadata']['source']}")
        print(f"Chunk Index: {result['metadata']['chunk_index']}")
        print(f"Distance: {result['vector_score']:.4f}")

        print("\nTEXT:\n")
        print(result["document"][:1000])

        print("\n")


if __name__ == "__main__":
    while True:
        query = input("\nQuery > ")

        if query.lower() in ["exit", "quit"]:
            break

        results = retrieve_vector(query)

        pretty_print(results)