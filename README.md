# Documentation Assistant

## 1) Project Brief Introduction
This project is an HTMX documentation assistant that uses a retrieval-augmented generation (RAG) pipeline plus an agentic routing flow. The goal is to answer technical questions using retrieved documentation while still supporting conversational follow-ups in a single, consistent assistant voice.

## 2) How to Run the Project
From the repo root:

```bash
cd backend
streamlit run ../frontend/streamlit_app.py
```

Make sure your backend `.venv` is active and `OPENAI_API_KEY` is set.

## 3) Agent Architecture (DAG Overview)
The assistant is orchestrated as a DAG (directed acyclic graph) with a single generator. The router inspects the full chat history and the current query, then decides whether retrieval is needed.

High-level flow:
- Router -> decides `rag` or `conversational`
- If `rag`: Retrieve -> Augment -> Generate
- If `conversational`: Generate

The generator always uses the same system prompt for a consistent voice. Retrieved chunks are not stored in chat history; only the final answer and metadata (e.g., citations) are saved.

## 4) RAG Pipeline Overview
The RAG pipeline is modular:
- Query rewrite (optional, history-aware)
- Hybrid retrieval (vector + BM25)
- Reranking (cross-encoder)
- Context assembly (augment node)
- Single generation step using the assembled context

Citations are derived from retrieved chunk metadata and attached to the assistant response without embedding chunk text into conversation memory.

## Data Initialization (One-time Setup)
Before running the assistant, make sure the documentation is crawled, processed into chunks, and indexed into ChromaDB. From the repo root:

```bash
cd backend
python -m app.crawler.crawler
python -m app.ingestion.processor
python -m app.retrieval.indexer
```

## Suggested Prompts
1. Create an example of HTMX for me 