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
