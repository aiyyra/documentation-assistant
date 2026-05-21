import chromadb


client = chromadb.PersistentClient(path="data/vectorstore")

collection = client.get_or_create_collection(
    name="htmx_docs"
)