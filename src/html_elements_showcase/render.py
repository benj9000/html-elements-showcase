from pathlib import Path

from jinja2 import Environment, PackageLoader, Template

from html_elements_showcase.configuration import (
    DIST_DIRECTORY,
    MDN_HTML_ELEMENTS_REFERENCE_URL,
    PROJECT_AUTHOR,
    PROJECT_NAME,
)
from html_elements_showcase.data_transfer_objects import SectionTemplateData


def render(sections: list[SectionTemplateData]) -> str:
    environment: Environment = Environment(
        loader=PackageLoader("html_elements_showcase"),
        autoescape=True,
    )
    template: Template = environment.get_template("base.html.jinja")
    context = {
        "author": PROJECT_AUTHOR,
        "title": PROJECT_NAME,
        "sections": sections,
        "attribution_url": MDN_HTML_ELEMENTS_REFERENCE_URL,
    }
    return template.render(context)


def write(content: str, filename: str = "index.html"):
    filepath: Path = DIST_DIRECTORY / filename
    _: int = filepath.write_text(content, encoding="utf-8")
    print(f"The rendered page has been written to {filepath.resolve()}.")
