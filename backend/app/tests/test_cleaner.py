from app.ingestion.cleaner import clean_markdown


# Reason:
# Cleaning is deterministic business logic.
# We want to ensure excessive whitespace normalization works correctly.
def test_clean_markdown_removes_excessive_newlines():
    raw_text = "Hello\n\n\n\nWorld"

    cleaned = clean_markdown(raw_text)

    assert cleaned == "Hello\n\nWorld"


# Reason:
# Leading/trailing whitespace should not survive preprocessing.
def test_clean_markdown_strips_whitespace():
    raw_text = "   Hello World   "

    cleaned = clean_markdown(raw_text)

    assert cleaned == "Hello World"