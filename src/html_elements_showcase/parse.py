from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from html_elements_showcase.data_transfer_objects import (
    ElementParseResult,
    SectionParseResult,
)


def _get_article_tag_from_page_source(page_source: str) -> Tag:
    soup: BeautifulSoup = BeautifulSoup(page_source, "html.parser")
    article: Tag | None = soup.select_one("article.main-page-content")
    if article is None:
        raise ValueError("Main page content not found.")
    return article


def _get_section_tags_from_article_tag(article_tag: Tag) -> ResultSet[Tag]:
    section_tags: ResultSet[Tag] = article_tag.select("section")
    if len(section_tags) == 0:
        raise ValueError("No section found in article.")
    return section_tags


def _parse_section_tags(section_tags: ResultSet[Tag]) -> list[SectionParseResult]:
    section_data: list[SectionParseResult] = []
    for section_tag in section_tags:
        if section_tag.attrs["aria-labelledby"] == "see_also":
            # The "See also" section does not contain any elements.
            continue
        h2: Tag | None = section_tag.h2
        if not h2:
            raise ValueError("No headline found for section.")
        headline: str = h2.text  # pyright: ignore[reportAny]

        description: str | None = _get_description_from_section_tag(section_tag)
        elements: list[ElementParseResult] = _get_elements_from_section_tag(section_tag)
        section_data.append(SectionParseResult(headline, description, elements))

    return section_data


def _get_description_from_section_tag(section_tag: Tag) -> str | None:
    paragraph_tag: Tag | None = section_tag.p
    if paragraph_tag:
        return paragraph_tag.text  # pyright: ignore[reportAny]
    return None


def _get_elements_from_section_tag(section_tag: Tag) -> list[ElementParseResult]:
    tbody_tag: Tag | None = section_tag.tbody
    if not tbody_tag:
        raise ValueError("No table found in section")
    tr_tags: ResultSet[Tag] = tbody_tag.select("tr")
    element_data: list[ElementParseResult] = []
    for tr_tag in tr_tags:
        td_tags: ResultSet[Tag] = tr_tag.select("td")
        if len(td_tags) != 2:
            raise ValueError("Unexpected number of cells in table row.")
        name_td_tag: Tag = td_tags[0]
        desc_td_tag: Tag = td_tags[1]
        element_name: str = name_td_tag.text  # pyright: ignore[reportAny]
        description: str = desc_td_tag.text  # pyright: ignore[reportAny]
        element_data.append(ElementParseResult(element_name, description))
    return element_data


def parse(page_source: str) -> list[SectionParseResult]:
    article_tag = _get_article_tag_from_page_source(page_source)
    sections_tags = _get_section_tags_from_article_tag(article_tag)
    return _parse_section_tags(sections_tags)
