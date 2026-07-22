from pathlib import Path

from app.parsers.csv_parser import CSVParser
from app.parsers.docx_parser import DocxParser
from app.parsers.excel_parser import ExcelParser
from app.parsers.json_parser import JsonParser
from app.parsers.markdown_parser import MarkdownParser
from app.parsers.pdf_parser import PDFParser
from app.parsers.pptx_parser import PowerPointParser
from app.parsers.txt_parser import TxtParser


class ParserFactory:

    PARSERS = {
        ".pdf": PDFParser,
        ".docx": DocxParser,
        ".txt": TxtParser,
        ".md": MarkdownParser,
        ".csv": CSVParser,
        ".xlsx": ExcelParser,
        ".xls": ExcelParser,
        ".pptx": PowerPointParser,
        ".json": JsonParser,
    }

    @classmethod
    def get_parser(cls, filename: str):

        extension = Path(filename).suffix.lower()

        parser = cls.PARSERS.get(extension)

        if parser is None:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return parser()