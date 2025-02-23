from pathlib import Path

import requests

from html_elements_showcase.configuration import (
    EXAMPLES_DIRECTORY,
    MDN_HTML_ELEMENTS_REFERENCE_CACHE_PATH,
    MDN_HTML_ELEMENTS_REFERENCE_URL,
)


def fetch_page_source() -> str:
    return requests.get(MDN_HTML_ELEMENTS_REFERENCE_URL).text


def fetch_page_source_debug() -> str:
    page_source: str
    if not MDN_HTML_ELEMENTS_REFERENCE_CACHE_PATH.exists():
        page_source = fetch_page_source()
        _: int = MDN_HTML_ELEMENTS_REFERENCE_CACHE_PATH.write_text(
            page_source, encoding="utf-8"
        )
    else:
        page_source = MDN_HTML_ELEMENTS_REFERENCE_CACHE_PATH.read_text()
    return page_source


def fetch_example(element_name: str) -> str | None:
    path: Path = EXAMPLES_DIRECTORY / f"{element_name}.html"
    if path.exists():
        return path.read_text()
    return None
