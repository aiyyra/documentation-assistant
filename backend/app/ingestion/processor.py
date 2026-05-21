import json
from pathlib import Path

from app.ingestion.cleaner import clean_markdown
from app.ingestion.chunker import chunk_document
from app.ingestion.schemas import Chunk


RAW_DIR = Path("data/raw/htmx")
OUTPUT_PATH = Path("data/processed/chunks/htmx_chunks.json")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_documents():
    documents = []

    for filepath in RAW_DIR.glob("*.md"):
        text = filepath.read_text(encoding="utf-8")

        documents.append(
            {
                "source": filepath.name,
                "text": text,
            }
        )

    return documents


def process_documents():
    processed_chunks = []

    documents = load_documents()

    print(f"[INFO] Loaded {len(documents)} documents")

    for doc in documents:
        source = doc["source"]

        cleaned_text = clean_markdown(doc["text"])

        chunks = chunk_document(cleaned_text)

        print(f"[INFO] {source} -> {len(chunks)} chunks")

        for idx, chunk_text in enumerate(chunks):
            chunk = Chunk(
                id=f"{source}_{idx}",
                text=chunk_text,
                source=source,
                chunk_index=idx,
            )

            processed_chunks.append(chunk.to_dict())

    return processed_chunks


def save_chunks(chunks):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"[SAVED] {OUTPUT_PATH}")


def main():
    chunks = process_documents()

    save_chunks(chunks)

    print(f"[DONE] Processed {len(chunks)} chunks")


if __name__ == "__main__":
    main()