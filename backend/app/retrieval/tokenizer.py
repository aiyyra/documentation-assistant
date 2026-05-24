import re


def tokenize(text: str) -> list[str]:
    text = text.lower()

    # Preserve:
    # - hyphens
    # - underscores
    # - colons
    #
    # Remove most other punctuation
    text = re.sub(
        r"[^a-z0-9\\s\-_:]",
        " ",
        text,
    )

    # Normalize whitespace
    text = re.sub(r"\\s+", " ", text)

    return text.strip().split()