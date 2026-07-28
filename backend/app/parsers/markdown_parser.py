from app.parsers.base_parser import BaseParser


class MarkdownParser(BaseParser):
    """
    Parser for Markdown (.md) files.
    """

    def extract_text(
        self,
        file_path: str,
    ) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            return file.read()