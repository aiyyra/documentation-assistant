from pathlib import Path
from urllib.parse import urlparse


OUTPUT_DIR = Path("data/raw/htmx")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def url_to_filename(url: str) -> str:
    path = urlparse(url).path.strip("/")

    if not path:
        return "index.md"

    filename = path.replace("/", "_")

    return f"{filename}.md"


def save_markdown(url: str, markdown: str):
    filename = url_to_filename(url)

    filepath = OUTPUT_DIR / filename

    filepath.write_text(markdown, encoding="utf-8")

    print(f"[SAVED] {filepath}")