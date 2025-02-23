from html_elements_showcase.data_transfer_objects import (
    ElementTemplateData,
    SectionParseResult,
    SectionTemplateData,
)
from html_elements_showcase.sanitize import sanitize_section


def _section_parse_result_to_section_template_data(
    section_parse_result: SectionParseResult,
) -> SectionTemplateData:
    sanitized_section_parse_result = sanitize_section(section_parse_result)

    element_template_data: list[ElementTemplateData] = []
    for element_parse_result in sanitized_section_parse_result.elements:
        element_template_data.append(
            ElementTemplateData(
                element_parse_result.name, element_parse_result.description, None
            )
        )
    return SectionTemplateData(
        sanitized_section_parse_result.headline,
        sanitized_section_parse_result.description,
        element_template_data,
    )


def parse_result_to_template_data(
    section_parse_result: list[SectionParseResult],
) -> list[SectionTemplateData]:
    return list(
        map(_section_parse_result_to_section_template_data, section_parse_result)
    )
