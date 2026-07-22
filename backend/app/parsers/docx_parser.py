from docx import Document

from app.parsers.base_parser import BaseParser


class DocxParser(BaseParser):
    """
    Parser for Microsoft Word (.docx) documents.
    """

    def extract_text(
        self,
        file_path: str,
    ) -> str:

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)