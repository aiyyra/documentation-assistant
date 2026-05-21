from sentence_transformers import SentenceTransformer


# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu",
)


def embed_text(texts: list[str]):
    return model.encode(texts, show_progress_bar=True)