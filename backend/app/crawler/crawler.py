from urllib.parse import urljoin, urlparse
from collections import deque

import httpx
from bs4 import BeautifulSoup

from app.crawler.parser import extract_markdown
from app.crawler.save import save_markdown


BASE_URL = "https://htmx.org"
START_URL = "https://htmx.org/docs/"

visited = set()


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)

    return (
        parsed.netloc == "htmx.org"
        and not parsed.fragment
        and not url.endswith(".xml")
    )


def get_links(html: str, current_url: str):
    soup = BeautifulSoup(html, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        full_url = urljoin(current_url, href)

        if is_valid_url(full_url):
            links.append(full_url)

    return links


def crawl():
    queue = deque([START_URL])

    with httpx.Client(timeout=10.0) as client:
        while queue:
            url = queue.popleft()

            if url in visited:
                continue

            print(f"[CRAWLING] {url}")

            visited.add(url)

            try:
                response = client.get(url)
                response.raise_for_status()

                html = response.text

                markdown = extract_markdown(html)

                save_markdown(url, markdown)

                links = get_links(html, url)

                for link in links:
                    if link not in visited:
                        queue.append(link)

            except Exception as e:
                print(f"[ERROR] {url} -> {e}")


if __name__ == "__main__":
    crawl()