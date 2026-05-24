from app.retrieval.tokenizer import tokenize


# Reason:
# Technical HTMX attributes must remain intact.
# Breaking these tokens severely hurts BM25 retrieval quality.
def test_tokenizer_preserves_htmx_attributes():
    text = "hx-trigger hx-swap-oob hx-push-url"

    tokens = tokenize(text)

    assert "hx-trigger" in tokens
    assert "hx-swap-oob" in tokens
    assert "hx-push-url" in tokens


# Reason:
# Special HTMX syntax should survive tokenization.
# These symbols are semantically meaningful in docs.
def test_tokenizer_preserves_colon_syntax():
    text = "hx-on::click"

    tokens = tokenize(text)

    assert "hx-on::click" in tokens


# Reason:
# Retrieval should be case-insensitive.
def test_tokenizer_lowercases_tokens():
    text = "HX-TRIGGER"

    tokens = tokenize(text)

    assert "hx-trigger" in tokens


# Reason:
# Obvious punctuation noise should be removed.
# Noise harms BM25 keyword matching quality.
def test_tokenizer_removes_punctuation_noise():
    text = "hx-trigger, hx-get."

    tokens = tokenize(text)

    assert "hx-trigger" in tokens
    assert "hx-get" in tokens

    assert "hx-trigger," not in tokens
    assert "hx-get." not in tokens


# Reason:
# Tokenizer should normalize excessive whitespace.
def test_tokenizer_normalizes_whitespace():
    text = "hx-trigger     hx-get"

    tokens = tokenize(text)

    assert tokens == [
        "hx-trigger",
        "hx-get",
    ]