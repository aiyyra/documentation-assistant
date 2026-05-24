from app.query.rewriter import (
    rewrite_query,
)


# Reason:
# Query rewriting should always return a string.
def test_rewriter_returns_string():
    rewritten = rewrite_query(
        "How do I trigger requests?"
    )

    assert isinstance(rewritten, str)


# Reason:
# Empty rewritten queries would break retrieval.
def test_rewriter_returns_non_empty_output():
    rewritten = rewrite_query(
        "How do I update HTML?"
    )

    assert len(rewritten.strip()) > 0