# Test Guide

This guide covers the automated test tiers and a manual system checklist.

## Automated Tests

### 1) Unit Tests (fast, CI-safe)
Run the mocked unit and integration graph tests only:

```bash
cd backend
pytest app/tests/test_agent_*.py app/tests/test_agent_graph_integration.py
```

### 2) Integration Tests (local data + model cache)
These require indexed chunks and local model downloads:

```bash
cd backend
RUN_INTEGRATION_TESTS=1 pytest -m integration
```

### 3) OpenAI-Dependent Tests (token usage)
These require `OPENAI_API_KEY` and will consume tokens:

```bash
cd backend
pytest -m openai
```

## Manual System Test Guide

This checklist validates end-to-end behavior: routing, retrieval quality, follow-ups, and the retry loop.

### How to Run
From the repo root:

```bash
cd backend
streamlit run ../frontend/streamlit_app.py
```

Make sure `OPENAI_API_KEY` is set and your data is indexed.

### Suggested Test Prompts (Grouped by Type)

#### 1) Conversational (no retrieval expected)
- "Hi, who are you?"
- "Thanks!"
- "Can you help me today?"
- "What did I ask earlier?"

#### 2) Direct HTMX definitions
- "What is HTMX?"
- "What is hx-post?"
- "What is hx-trigger?"
- "What does hx-swap do?"

#### 3) Practical usage (how-to)
- "How do I use hx-post in a form?"
- "How do I load a partial into a target div?"
- "How do I trigger a request on page load?"
- "How do I update part of the DOM without JS?"

#### 4) Follow-up / coreference (tests history + routing)
Step A: "What is hx-post?"
Step B: "What about that attribute in a form?"

Step A: "How do I swap content?"
Step B: "Can I change the swap strategy?"

#### 5) Edge / ambiguous (tests router + evaluator loop)
- "What is the best way to do it?"
- "Explain this."
- "Make it faster."

#### 6) Out-of-scope (should not hallucinate)
- "How do I configure nginx reverse proxy?"
- "What’s the best React state library?"
- "Explain Redis persistence"

### What to Check (Quick Checklist)
- Router behavior: conversational prompts should not trigger retrieval.
- RAG behavior: HTMX prompts should return citations.
- Follow-ups: answers should refer to prior context.
- No chunk leakage: chat history should not include raw retrieved chunks.
- Retry loop: if an answer is weak or ungrounded, the system retries once.

### Notes
- If a result looks off, note the question and whether the route was `rag` or `conversational`.
- Use citations to confirm grounding quality.
