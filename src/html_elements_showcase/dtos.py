from dataclasses import dataclass


@dataclass
class ElementParseResult:
    name: str
    description: str


@dataclass
class SectionParseResult:
    headline: str
    description: str | None
    elements: list[ElementParseResult]


@dataclass
class ElementTemplateData:
    name: str
    description: str
    example: str | None


@dataclass
class SectionTemplateData:
    headline: str
    description: str | None
    elements: list[ElementTemplateData]
