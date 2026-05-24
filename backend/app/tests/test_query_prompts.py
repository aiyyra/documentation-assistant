from app.query.prompts import (
    build_rewrite_prompt,
)


# Reason:
# Prompt should include original user query.
def test_rewrite_prompt_contains_query():
    query = "How do I update HTML?"

    prompt = build_rewrite_prompt(query)

    assert query in prompt


# Reason:
# Rewrite prompt must strongly constrain the model
# to avoid answering instead of rewriting.
def test_rewrite_prompt_contains_constraints():
    prompt = build_rewrite_prompt(
        "test query"
    )

    assert "Do NOT answer the question" in prompt

    assert "Return ONLY the rewritten query" in prompt