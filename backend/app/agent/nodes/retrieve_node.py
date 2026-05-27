from app.agent.utils import format_history
from app.generation.citations import build_citations
from app.query.rewriter import (
    rewrite_query,
    rewrite_query_with_history,
)
from app.retrieval.hybrid_retriever import hybrid_retrieve
from app.retrieval.reranker import rerank_results


RERANK_THRESHOLD = -0.2
RERANK_FALLBACK_MIN = 2


def retrieve_node(state):
    query = state["query"]
    chat_history = state.get("chat_history")
    retry_reason = state.get("retry_reason")

    query_for_rewrite = (
        f"{query}\n{retry_reason}"
        if retry_reason
        else query
    )

    history_text = format_history(chat_history)

    if history_text:
        retrieval_query = rewrite_query_with_history(
            query_for_rewrite,
            history_text,
        )
    else:
        retrieval_query = rewrite_query(
            query_for_rewrite
        )

    retrieval_results = hybrid_retrieve(
        query=retrieval_query,
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

    filtered_reranked = [
        item
        for item in reranked
        if item["rerank_score"] >= RERANK_THRESHOLD
    ]
    if len(filtered_reranked) < RERANK_FALLBACK_MIN:
        filtered_reranked = reranked[:RERANK_FALLBACK_MIN]

    reranked_documents = [
        item["document"]
        for item in filtered_reranked
    ]

    reranked_metadata = [
        item["metadata"]
        for item in filtered_reranked
    ]

    citations = build_citations(
        reranked_metadata
    )

    return {
        **state,
        "route": "rag",
        "used_rag": True,
        "rewritten_query": retrieval_query,
        "retrieved_chunks": reranked_documents,
        "citations": citations,
        "retrieval_results": retrieval_results,
        "reranked_results": reranked,
    }
