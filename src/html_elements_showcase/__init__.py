from html_elements_showcase.build import build
from html_elements_showcase.configuration import is_debug_mode_enabled


def main() -> None:
    build(debug=is_debug_mode_enabled())
