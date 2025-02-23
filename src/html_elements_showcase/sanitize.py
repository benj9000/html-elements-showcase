import re

from html_elements_showcase.data_transfer_objects import (
    ElementParseResult,
    SectionParseResult,
)


def _remove_angle_brackets(string: str) -> str:
    return re.sub(r"[<>]", "", string).strip()


def _collapse_whitespace(string: str) -> str:
    return re.sub(r"\s+", " ", string).strip()


def _sanitize_element(element: ElementParseResult) -> ElementParseResult:
    name: str = _collapse_whitespace(element.name)
    description: str = _collapse_whitespace(element.description)
    return ElementParseResult(name, description)


def sanitize_section(section: SectionParseResult) -> SectionParseResult:
    headline: str = _collapse_whitespace(section.headline)
    description: str | None = None
    if section.description:
        description = _collapse_whitespace(section.description)
    elements: list[ElementParseResult] = list(map(_sanitize_element, section.elements))
    return SectionParseResult(headline, description, elements)
