import os

import pytest

from app.query.rewriter import (
    rewrite_query,
)


@pytest.mark.openai
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set",
)
def test_rewriter_returns_string():
    rewritten = rewrite_query(
        "How do I trigger requests?"
    )

    assert isinstance(rewritten, str)


@pytest.mark.openai
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set",
)
def test_rewriter_returns_non_empty_output():
    rewritten = rewrite_query(
        "How do I update HTML?"
    )

    assert len(rewritten.strip()) > 0