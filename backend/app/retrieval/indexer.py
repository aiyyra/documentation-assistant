import json
from pathlib import Path

from app.retrieval.embedder import embed_text
from app.retrieval.vectordb import collection


CHUNK_PATH = Path("data/processed/chunks/htmx_chunks.json")


def load_chunks():
    with open(CHUNK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def index_chunks():
    chunks = load_chunks()

    print(f"[INFO] Loaded {len(chunks)} chunks")

    texts = [chunk["text"] for chunk in chunks]

    print("[INFO] Generating embeddings...")

    embeddings = embed_text(texts)

    print("[INFO] Storing embeddings in ChromaDB...")

    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ],
    )

    print("[DONE] Indexing complete")


if __name__ == "__main__":
    index_chunks()