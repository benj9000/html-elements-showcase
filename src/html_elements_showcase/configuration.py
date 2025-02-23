from pathlib import Path

PROJECT_NAME: str = "HTML Elements Showcase"
PROJECT_AUTHOR: str = "benj9000"

PROJECT_ROOT: Path = Path(__file__).parents[2]
DATA_DIRECTORY: Path = PROJECT_ROOT / "data"
EXAMPLES_DIRECTORY: Path = DATA_DIRECTORY / "examples"
DIST_DIRECTORY: Path = PROJECT_ROOT / "dist"

MDN_HTML_ELEMENTS_REFERENCE_URL: str = (
    "https://developer.mozilla.org/en-US/docs/Web/HTML/Element"
)
MDN_HTML_ELEMENTS_REFERENCE_CACHE_PATH: Path = (
    DATA_DIRECTORY / "mdn-html-elements-reference.html"
)

DEBUG: bool = True
