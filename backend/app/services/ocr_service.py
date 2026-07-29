import os
import tempfile

import cv2
import easyocr

from app.core.config import settings


class OCRService:
    _reader = None

    @classmethod
    def get_reader(cls):
        if cls._reader is None:
            print("Loading EasyOCR model...")

            cls._reader = easyocr.Reader(
                ["en"],
                gpu=False,
            )

        return cls._reader

    @staticmethod
    def _deskew(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        coords = cv2.findNonZero(255 - gray)

        if coords is None:
            return image

        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = 90 + angle

        h, w = image.shape[:2]

        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0,
        )

        return cv2.warpAffine(
            image,
            matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )

    @classmethod
    def extract_text(cls, image_path: str) -> str:

        if settings.OCR_ENGINE == "easyocr":
            return cls._extract_easyocr(image_path)

        if settings.OCR_ENGINE == "paddleocr":
            return cls._extract_paddleocr(image_path)

        raise ValueError(
            f"Unsupported OCR engine: {settings.OCR_ENGINE}"
        )

    @classmethod
    def _extract_easyocr(cls, image_path: str) -> str:

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Unable to read image: {image_path}")

        # -----------------------------
        # Deskew
        # -----------------------------
        image = cls._deskew(image)

        # -----------------------------
        # Upscale
        # -----------------------------
        image = cv2.resize(
            image,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC,
        )

        # -----------------------------
        # Grayscale
        # -----------------------------
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        # -----------------------------
        # Denoise
        # -----------------------------
        gray = cv2.fastNlMeansDenoising(gray)

        # -----------------------------
        # Improve contrast
        # -----------------------------
        gray = cv2.equalizeHist(gray)

        # -----------------------------
        # Adaptive Threshold
        # -----------------------------
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            11,
        )

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False,
            ) as temp:

                temp_path = temp.name

            cv2.imwrite(temp_path, thresh)

            reader = cls.get_reader()

            results = reader.readtext(
                temp_path,
                detail=1,
                paragraph=True,
                decoder="beamsearch",
                batch_size=4,
            )

            lines = []

            for _, text, confidence in results:

                if confidence >= 0.40:
                    lines.append(text)

            print(
                f"OCR extracted {len(lines)} lines from "
                f"{os.path.basename(image_path)}"
            )

            return "\n".join(lines)

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    @classmethod
    def _extract_paddleocr(cls, image_path: str) -> str:
        raise NotImplementedError(
            "PaddleOCR support is not implemented yet."
        )