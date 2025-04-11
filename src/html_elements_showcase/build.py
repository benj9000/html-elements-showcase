import shutil
from pathlib import Path

from html_elements_showcase.configuration import (
    Location,
    MetaData,
    get_output_directory,
)
from html_elements_showcase.dtos import SectionParseResult, SectionTemplateData
from html_elements_showcase.fetch import fetch_page_source, fetch_page_source_debug
from html_elements_showcase.parse import parse
from html_elements_showcase.render import render
from html_elements_showcase.transfer import parse_result_to_template_data


def _prepare_output_directory(directory: Path, debug: bool) -> None:
    _validate_output_directory(directory)
    if not _is_output_directory_clean(directory):
        if debug:
            _clean_output_directory(directory)
        else:
            raise ValueError(f"The output directory {directory} is not clean.")


def _validate_output_directory(directory: Path) -> None:
    if not directory.exists():
        raise FileNotFoundError(f"The output directory {directory} does not exist.")
    if not directory.is_dir():
        raise NotADirectoryError(
            f"The output directory {directory} is not a directory."
        )


def _is_output_directory_clean(directory: Path) -> bool:
    directory_content: list[Path] = list(directory.glob("*"))
    return len(directory_content) == 1 and directory_content[0].name == ".gitkeep"


def _clean_output_directory(directory: Path) -> None:
    for path in directory.iterdir():
        if path.name == ".gitkeep":
            continue

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def _fetch_page_source(debug: bool) -> str:
    if debug:
        return fetch_page_source_debug()
    else:
        return fetch_page_source()


def _process_page_source(page_source: str) -> str:
    sections: list[SectionParseResult] = parse(page_source)
    template_data: list[SectionTemplateData] = parse_result_to_template_data(sections)
    return render(template_data)


def _write_output(
    output_directory: Path,
    output_name: str,
    output_content: str,
    example_assets_directory: Path,
) -> None:
    output_subdirectory: Path = output_directory / output_name
    output_subdirectory.mkdir()
    _write_page(output_content, output_subdirectory)
    shutil.copytree(example_assets_directory, output_subdirectory / "assets")


def _write_page(content: str, destination: Path, filename: str = "index.html") -> None:
    filepath: Path = destination / filename
    _: int = filepath.write_text(content, encoding="utf-8")
    print(f"The rendered page has been written to {filepath.resolve()}.")


def build(debug: bool) -> None:
    output_directory: Path = get_output_directory()
    _prepare_output_directory(output_directory, debug)
    page_source: str = _fetch_page_source(debug)
    output_page_source: str = _process_page_source(page_source)
    _write_output(
        output_directory,
        MetaData.PROJECT_NAME.value,
        output_page_source,
        Location.EXAMPLE_ASSETS_DIRECTORY.value,
    )
