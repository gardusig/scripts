from dataclasses import dataclass
from typing import Any
import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class HtmlData:
    url: str
    title: str
    meta: dict[str, Any]
    links: list[str]
    text: str


def extract_html_data(url: str) -> HtmlData:
    """
    Fetches a URL, parses its HTML, and extracts relevant data.
    Returns a dictionary with title, meta tags, links, and visible text.
    """
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    meta: dict[str, Any] = {}
    for tag in soup.find_all("meta"):
        if isinstance(tag, Tag):
            if tag.get("name") and tag.get("content"):
                meta[tag["name"]] = tag["content"]
            elif tag.get("property") and tag.get("content"):
                meta[tag["property"]] = tag["content"]

    links = []
    for el in soup.find_all("a"):
        if isinstance(el, Tag):
            href = el.get("href")
            if href:
                links.append(href)

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator="\n", strip=True)

    return HtmlData(url=url, title=title, meta=meta, links=links, text=text)
