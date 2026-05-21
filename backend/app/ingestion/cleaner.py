import re


def clean_markdown(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)

    text = text.strip()

    return text