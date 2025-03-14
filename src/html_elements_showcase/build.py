import shutil
from pathlib import Path

from html_elements_showcase.configuration import (
    EXAMPLE_ASSETS_DIRECTORY,
    OUTPUT_ASSETS_DIRECTORY,
    OUTPUT_DIRECTORY,
)
from html_elements_showcase.dtos import SectionParseResult, SectionTemplateData
from html_elements_showcase.fetch import fetch_page_source, fetch_page_source_debug
from html_elements_showcase.parse import parse
from html_elements_showcase.render import render
from html_elements_showcase.transfer import parse_result_to_template_data


def _write_page(content: str, destination: Path, filename: str = "index.html") -> None:
    filepath: Path = destination / filename
    _: int = filepath.write_text(content, encoding="utf-8")
    print(f"The rendered page has been written to {filepath.resolve()}.")


def _copy_assets(source: Path, destination: Path) -> None:
    destination.mkdir()
    for file in source.iterdir():
        shutil.copy(file, destination)


def _is_output_directory_empty(directory: Path) -> bool:
    if not directory.exists():
        raise ValueError("Directory does not exist.")
    if directory.is_file():
        raise ValueError("Directory is actually a file.")

    directory_content: list[Path] = list(directory.glob("*"))
    return len(directory_content) == 1 and directory_content[0].name == ".gitkeep"


def _clean_output_directory(directory: Path) -> None:
    if not directory.exists():
        raise FileNotFoundError(f"Directory {directory} does not exist.")
    if not directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory.")

    for path in directory.iterdir():
        if path.name == ".gitkeep":
            continue

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def build(debug: bool) -> None:
    if not _is_output_directory_empty(OUTPUT_DIRECTORY):
        if debug:
            _clean_output_directory(OUTPUT_DIRECTORY)
        else:
            raise ValueError(f"The output directory ({OUTPUT_DIRECTORY}) is not empty.")

    page_source: str
    if debug:
        page_source = fetch_page_source_debug()
    else:
        page_source = fetch_page_source()

    sections: list[SectionParseResult] = parse(page_source)
    template_data: list[SectionTemplateData] = parse_result_to_template_data(sections)
    content: str = render(template_data)

    _write_page(content, OUTPUT_DIRECTORY)
    _copy_assets(EXAMPLE_ASSETS_DIRECTORY, OUTPUT_ASSETS_DIRECTORY)
