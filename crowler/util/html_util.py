from typing import Optional, Set
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import typer


def is_valid_url(url: str) -> bool:
    """Check if a URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        print(e)
        return False


def extract_data_from_html(url: str) -> Set[str]:
    """Extract links from an HTML page."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        # TODO extract all texts and urls from html, like this has a text within: "like a task details website, to extract relevant links and data from it"
        # <div class="IssueBodyViewer-module__IssueBody--MXyFt"><div data-testid="markdown-body" data-team-hovercards-enabled="true" class="markdown-body" data-turbolinks="false"><div class="Box-sc-g0xbh4-0 markdown-body NewMarkdownViewer-module__safe-html-box--cRsz0"><p dir="auto">accept urls as a source of data to GET through their html content</p>
        # <ul dir="auto">
        # <li>like a task details website, to extract relevant links and data from it</li>
        # </ul></div></div><div class="IssueBodyViewer-module__IssueBodyTaskList--r4XEH"><div class="IssueBodyViewer-module__IssueBodySubIssueButtonContainer--EZm50"><div class="AddSubIssueButtonGroup-module__Box--Txhdj"><div class="d-none"></div><div class="Box-sc-g0xbh4-0 prc-ButtonGroup-ButtonGroup-vcMeG"><div><button type="button" class="prc-Button-ButtonBase-c50BI" data-loading="false" data-no-visuals="true" data-size="small" data-variant="default" aria-describedby=":rk:-loading-announcement"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-HKbr-"><span data-component="text" class="prc-Button-Label-pTQ3x">Create sub-issue</span></span></button></div><div><button data-component="IconButton" type="button" aria-label="View more sub-issue options" class="prc-Button-ButtonBase-c50BI prc-Button-IconButton-szpyj" data-loading="false" data-no-visuals="true" data-size="small" data-variant="default" aria-describedby=":rl:-loading-announcement"><svg aria-hidden="true" focusable="false" class="octicon octicon-triangle-down" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align: text-bottom;"><path d="m4.427 7.427 3.396 3.396a.25.25 0 0 0 .354 0l3.396-3.396A.25.25 0 0 0 11.396 7H4.604a.25.25 0 0 0-.177.427Z"></path></svg></button></div></div></div></div><div role="toolbar" aria-label="Reactions" class="d-flex gap-1 flex-wrap"><button data-component="IconButton" type="button" aria-label="Add or remove reactions" aria-haspopup="true" aria-expanded="false" tabindex="0" class="Box-sc-g0xbh4-0 hRifVb prc-Button-ButtonBase-c50BI prc-Button-IconButton-szpyj" data-loading="false" data-no-visuals="true" data-size="small" data-variant="default" aria-describedby=":r2r:-loading-announcement" id=":r2r:"><svg aria-hidden="true" focusable="false" class="octicon octicon-smiley" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align: text-bottom;"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm3.82 1.636a.75.75 0 0 1 1.038.175l.007.009c.103.118.22.222.35.31.264.178.683.37 1.285.37.602 0 1.02-.192 1.285-.371.13-.088.247-.192.35-.31l.007-.008a.75.75 0 0 1 1.222.87l-.022-.015c.02.013.021.015.021.015v.001l-.001.002-.002.003-.005.007-.014.019a2.066 2.066 0 0 1-.184.213c-.16.166-.338.316-.53.445-.63.418-1.37.638-2.127.629-.946 0-1.652-.308-2.126-.63a3.331 3.331 0 0 1-.715-.657l-.014-.02-.005-.006-.002-.003v-.002h-.001l.613-.432-.614.43a.75.75 0 0 1 .183-1.044ZM12 7a1 1 0 1 1-2 0 1 1 0 0 1 2 0ZM5 8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm5.25 2.25.592.416a97.71 97.71 0 0 0-.592-.416Z"></path></svg></button></div></div></div>

        return links
    except Exception as e:
        typer.secho(f"Error extracting links from {url}: {e}", fg="red")
        return set()
