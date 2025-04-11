import os
from enum import Enum, auto
from pathlib import Path
from typing import override


class MetaData(Enum):
    """Metadata about the project."""

    PROJECT_NAME = "html-elements-showcase"
    PROJECT_AUTHOR = "benj9000"
    PROJECT_NAME_HUMAN_READABLE = "HTML Elements Showcase"


class Source(Enum):
    """References to data sources."""

    MDN_HTML_ELEMENTS_REFERENCE_URL = (
        "https://developer.mozilla.org/en-US/docs/Web/HTML/Element"
    )


class Location(Enum):
    """Locations relative to the project's root."""

    PROJECT_ROOT_DIRECTORY = Path(__file__).parents[2]
    DATA_DIRECTORY = PROJECT_ROOT_DIRECTORY / "data"
    EXAMPLES_DIRECTORY = DATA_DIRECTORY / "examples"
    EXAMPLE_ASSETS_DIRECTORY = EXAMPLES_DIRECTORY / "assets"
    OUTPUT_DIRECTORY = PROJECT_ROOT_DIRECTORY / "dist"
    SOURCE_CACHE_FILE = DATA_DIRECTORY / "mdn-html-elements-reference.html"


class EnvVariable(Enum):
    """Environment variable names."""

    @override
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> str:
        PREFIX: str = "HES"
        return f"{PREFIX}_{name}"

    OUT_DIR = auto()
    """Name of the environment variable to set the output directory."""
    DEBUG = auto()
    """Name of the environment variable to set debug mode."""


def get_output_directory() -> Path:
    """Get the path to the directory where the output will be placed."""
    env_value: str | None = os.environ.get(EnvVariable.OUT_DIR.value)
    if env_value:
        path_from_env: Path = Path(env_value)
        if path_from_env.is_dir():
            return path_from_env
        raise ValueError("Invalid path.")

    raise ValueError("Output directory not defined.")


def is_debug_mode_enabled() -> bool:
    """Whether the debug mode is enabled."""
    env_value: str | None = os.environ.get(EnvVariable.DEBUG.value)
    if env_value and env_value in ["false", "0"]:
        return False

    return True
