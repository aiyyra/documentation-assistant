from app.retrieval.embedder import embed_text
from app.retrieval.vectordb import collection


def retrieve(query: str, top_k: int = 5):
    query_embedding = embed_text([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
    )

    return results


def pretty_print(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for idx, (doc, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        print("=" * 80)

        print(f"[RESULT {idx}]")
        print(f"Source: {metadata['source']}")
        print(f"Chunk Index: {metadata['chunk_index']}")
        print(f"Distance: {distance:.4f}")

        print("\nTEXT:\n")
        print(doc[:1000])

        print("\n")


if __name__ == "__main__":
    while True:
        query = input("\nQuery > ")

        if query.lower() in ["exit", "quit"]:
            break

        results = retrieve(query)

        pretty_print(results)