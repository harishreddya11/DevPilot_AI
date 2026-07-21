from fastapi import APIRouter

from app.services.embedding_service import EmbeddingService

router = APIRouter(prefix="/test", tags=["Test"])

embedding_service = EmbeddingService()


@router.get("/embedding")
async def test_embedding():
    embedding = await embedding_service.generate_embedding(
        "DevPilot AI is awesome!"
    )

    return {
        "dimensions": len(embedding),
        "sample": embedding[:5],
    }