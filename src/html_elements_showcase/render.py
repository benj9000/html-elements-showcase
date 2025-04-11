from jinja2 import Environment, PackageLoader, Template

from html_elements_showcase.configuration import MetaData, Source
from html_elements_showcase.dtos import SectionTemplateData


def render(sections: list[SectionTemplateData]) -> str:
    environment: Environment = Environment(
        loader=PackageLoader("html_elements_showcase"),
        autoescape=True,
    )
    template: Template = environment.get_template("base.html.jinja")
    context = {
        "author": MetaData.PROJECT_AUTHOR.value,
        "title": MetaData.PROJECT_NAME_HUMAN_READABLE.value,
        "sections": sections,
        "attribution_url": Source.MDN_HTML_ELEMENTS_REFERENCE_URL.value,
    }
    return template.render(context)
