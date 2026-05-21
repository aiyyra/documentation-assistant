from app.retrieval.retriever import retrieve
from app.generation.prompt import build_prompt
from app.generation.generator import generate_response


def ask(query: str):
    retrieval_results = retrieve(query)

    documents = retrieval_results["documents"][0]

    response_prompt = build_prompt(
        query=query,
        retrieved_chunks=documents,
    )

    answer = generate_response(response_prompt)

    return {
        "answer": answer,
        "documents": documents,
        "metadata": retrieval_results["metadatas"][0],
    }