import json

from app.parsers.base_parser import BaseParser


class JsonParser(BaseParser):
    """
    Parser for JSON files.
    """

    def extract_text(
        self,
        file_path: str,
    ) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        )