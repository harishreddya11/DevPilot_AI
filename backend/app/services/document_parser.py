from pathlib import Path
from pypdf import PdfReader
from docx import Document


class DocumentParser:

    @staticmethod
    def extract_text(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            reader = PdfReader(file_path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)

        elif extension == ".docx":
            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        raise ValueError("Unsupported file type")