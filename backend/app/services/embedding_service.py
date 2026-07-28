"""
Embedding Service

Generates vector embeddings for text chunks.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )
        return cls._model

    @classmethod
    def generate_embedding(cls, text: str) -> list[float]:
        """
        Generate embedding for a single text.
        """
        model = cls.get_model()

        embedding = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    @classmethod
    def generate_embeddings(cls, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        model = cls.get_model()

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()