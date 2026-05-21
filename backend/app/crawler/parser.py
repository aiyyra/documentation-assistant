from bs4 import BeautifulSoup
from markdownify import markdownify as md


def extract_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main = soup.find("main")

    if not main:
        main = soup.body

    cleaned_html = str(main)

    markdown = md(cleaned_html)

    return markdown