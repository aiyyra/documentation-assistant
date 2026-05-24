from app.retrieval.vector_retriever import retrieve
from app.retrieval.reranker import rerank_results

from app.generation.prompt import build_prompt
from app.generation.generator import generate_response


def ask(query: str):
    retrieval_results = retrieve(
        query=query,
        top_k= 15
    )

    documents = retrieval_results["documents"][0]
    metadatas = retrieval_results["metadatas"][0]

    reranked = rerank_results(
        query=query,
        documents=documents,
        metadatas=metadatas,
        top_n=5,
    )

    # Temp print statement to add visibality on ranking score
    for item in reranked:
        print(item["rerank_score"])

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
    }