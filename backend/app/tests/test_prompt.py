from app.generation.prompt import build_prompt


# Reason:
# Prompt construction is deterministic logic.
# We verify user queries are inserted correctly.
def test_prompt_contains_query():
    query = "What is hx-trigger?"

    prompt = build_prompt(query, ["sample context"])

    assert query in prompt


# Reason:
# Retrieved chunks must actually appear inside the prompt.
# Otherwise retrieval becomes useless.
def test_prompt_contains_context_chunks():
    chunks = [
        "hx-trigger allows events",
        "hx-get performs GET requests",
    ]

    prompt = build_prompt(
        query="test",
        retrieved_chunks=chunks,
    )

    assert chunks[0] in prompt
    assert chunks[1] in prompt


# Reason:
# Grounding instructions are critical for reducing hallucinations.
def test_prompt_contains_grounding_instruction():
    prompt = build_prompt(
        query="test",
        retrieved_chunks=["context"],
    )

    assert "ONLY using the provided context" in prompt