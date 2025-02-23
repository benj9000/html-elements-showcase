from html_elements_showcase.configuration import DEBUG
from html_elements_showcase.dtos import SectionParseResult, SectionTemplateData
from html_elements_showcase.fetch import (
    fetch_page_source,
    fetch_page_source_debug,
)
from html_elements_showcase.parse import parse
from html_elements_showcase.render import render, write
from html_elements_showcase.transfer import parse_result_to_template_data


def build(debug: bool) -> None:
    page_source: str
    if debug:
        page_source = fetch_page_source_debug()
    else:
        page_source = fetch_page_source()
    sections: list[SectionParseResult] = parse(page_source)
    template_data: list[SectionTemplateData] = parse_result_to_template_data(sections)
    content: str = render(template_data)
    write(content)


def main() -> None:
    build(debug=DEBUG)
