"""
Image Parser

Supports:
- PNG
- JPG
- JPEG
- BMP
- TIFF
- WEBP

Extracts text using OCRService (EasyOCR).
"""

from app.parsers.base_parser import BaseParser
from app.services.ocr_service import OCRService


class ImageParser(BaseParser):
    """
    Parser for image files.

    Supported formats:
        - .png
        - .jpg
        - .jpeg
        - .bmp
        - .tiff
        - .webp
    """

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from an image using OCR.

        Args:
            file_path (str): Absolute path to the image.

        Returns:
            str: Extracted text.
        """
        return OCRService.extract_text(file_path)