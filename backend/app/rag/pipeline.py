from app.retrieval.hybrid_retriever import (
    hybrid_retrieve,
)

from app.retrieval.reranker import (
    rerank_results,
)

from app.generation.prompt import build_prompt
from app.generation.generator import generate_response


def ask(query: str):
    retrieval_results = hybrid_retrieve(
        query=query,
        vector_top_k=10,
        bm25_top_k=10,
    )

    documents = [
        result["document"]
        for result in retrieval_results
    ]

    metadatas = [
        result["metadata"]
        for result in retrieval_results
    ]

    reranked = rerank_results(
        query=query,
        documents=documents,
        metadatas=metadatas,
        top_n=5,
    )

    # filter rerank score that are below threshold
    filtered_reranked = [
        item
        for item in reranked
        if item["rerank_score"] >= -0.2
    ]
    if len(filtered_reranked) < 2:
        filtered_reranked = reranked[:2]

    # Temporary debugging visibility
    for item in reranked:
        print(
            f"[RERANK SCORE] "
            f"{item['rerank_score']:.4f}"
        )

    reranked_documents = [
        item["document"]
        for item in reranked
    ]

    reranked_metadata = [
        item["metadata"]
        for item in reranked
    ]

    response_prompt = build_prompt(
        query=query,
        retrieved_chunks=reranked_documents,
    )

    answer = generate_response(response_prompt)

    return {
        "answer": answer,
        "documents": reranked_documents,
        "metadata": reranked_metadata,
        "retrieval_results": retrieval_results,
        "reranked_results": reranked,
    }