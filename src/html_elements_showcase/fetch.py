from pathlib import Path

import requests

from html_elements_showcase.configuration import Location, Source

PAGE_SOURCE_ENCODING: str = "utf-8"


def fetch_page_source() -> str:
    response = requests.get(Source.MDN_HTML_ELEMENTS_REFERENCE_URL.value)
    # The encoding is not detected correctly automatically, such that we have to set it explicitly.
    response.encoding = PAGE_SOURCE_ENCODING
    return response.text


def fetch_page_source_debug() -> str:
    page_source: str
    if not Location.SOURCE_CACHE_FILE.value.exists():
        page_source = fetch_page_source()
        _: int = Location.SOURCE_CACHE_FILE.value.write_text(
            page_source, encoding=PAGE_SOURCE_ENCODING
        )
    else:
        page_source = Location.SOURCE_CACHE_FILE.value.read_text()
    return page_source


def fetch_example(element_name: str) -> str | None:
    path: Path = Location.EXAMPLES_DIRECTORY.value / f"{element_name}.html"
    if path.exists():
        return path.read_text()
    return None
