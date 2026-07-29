import fitz
import os
import tempfile

from numpy import matrix

from app.parsers.base_parser import BaseParser
from app.services.ocr_service import OCRService


class PDFParser(BaseParser):

    def extract_text(self, file_path: str) -> str:
        document = fitz.open(file_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        text = "\n".join(pages).strip()

        if text:
            document.close()
            return text

        ocr_pages = []

        with tempfile.TemporaryDirectory() as temp_dir:

            for page_number, page in enumerate(document):

                matrix = fitz.Matrix(300 / 72, 300 / 72)
                pix = page.get_pixmap(matrix=matrix)

                image_path = os.path.join(
                    temp_dir,
                    f"page_{page_number}.png",
                )

                pix.save(image_path)

                page_text = OCRService.extract_text(image_path)

                ocr_pages.append(page_text)

        document.close()

        return "\n".join(ocr_pages)