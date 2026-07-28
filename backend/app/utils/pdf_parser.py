from pathlib import Path

from pypdf import PdfReader


class PDFParser:
    @staticmethod
    def extract_text(file_path: str) -> str:
        reader = PdfReader(Path(file_path))

        pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        return "\n".join(pages)