import fitz
from fastapi import UploadFile

from app.parsers.base_parser import BaseParser


class PDFParser(BaseParser):

    def extract_text(self, file_path: str) -> str:
        document = fitz.open(file_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)