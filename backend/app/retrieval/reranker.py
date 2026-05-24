from sentence_transformers import CrossEncoder


reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    device="cpu",
)


def rerank_results(
    query: str,
    documents: list[str],
    metadatas: list[dict],
    top_n: int = 5,
):
    pairs = [
        [query, document]
        for document in documents
    ]

    scores = reranker_model.predict(pairs)

    reranked = []

    for doc, metadata, score in zip(
        documents,
        metadatas,
        scores,
    ):
        reranked.append(
            {
                "document": doc,
                "metadata": metadata,
                "rerank_score": float(score),
            }
        )

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True,
    )

    
    return reranked[:top_n]