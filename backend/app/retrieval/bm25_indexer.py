import json
from pathlib import Path

from rank_bm25 import BM25Okapi
from app.retrieval.tokenizer import tokenize


CHUNK_PATH = Path(
    "data/processed/chunks/htmx_chunks.json"
)


def load_chunks():
    with open(CHUNK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


chunks = load_chunks()

tokenized_chunks = [
    # we can further imrpove tokenization later
    tokenize(chunk["text"])
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_chunks)