from typing import List, Optional, Set
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import typer


def is_valid_url(url: str) -> bool:
    """Check if a URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def extract_links_from_html(url: str, base_domain: Optional[str] = None) -> Set[str]:
    """Extract links from an HTML page."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        if not base_domain:
            parsed_url = urlparse(url)
            base_domain = parsed_url.netloc


        for a_tag in soup.find_all('a'):
            if isinstance(a_tag, Tag) and a_tag.has_attr('href'):
                href = a_tag.get('href')
                if href:
                    full_url = urljoin(url, href)
                    parsed_full_url = urlparse(full_url)
                    if parsed_full_url.netloc == base_domain and is_valid_url(full_url):
                        links.add(full_url)

        return links
    except Exception as e:
        typer.secho(f"Error extracting links from {url}: {e}", fg="red")
        return set()


def crawl_and_extract_links(
    start_urls: List[str],
    depth: int = 1,
    max_links: int = 10
) -> List[str]:
    """Crawl HTML links and extract new links from them."""
    all_links = set(start_urls)
    to_visit = set(start_urls)
    visited = set()
    new_links = set()
    for _ in range(depth):
        if not to_visit or len(all_links) >= max_links:
            break
        current_level = list(to_visit)
        to_visit = set()
        for url in current_level:
            if url in visited or len(all_links) >= max_links:
                continue
            typer.secho(f"Crawling: {url}", fg="blue")
            visited.add(url)
            extracted_links = extract_links_from_html(url)
            for link in extracted_links:
                if link not in all_links and link not in visited:
                    to_visit.add(link)
                    all_links.add(link)
                    new_links.add(link)
                    if len(all_links) >= max_links:
                        break
    return list(new_links)
