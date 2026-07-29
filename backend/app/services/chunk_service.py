from typing import List


class ChunkingService:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @classmethod
    def chunk_text(
        cls,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> List[str]:
        return cls(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        ).split_text(text)

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []

        text = text.strip()
        chunks = []

        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap

        return chunks