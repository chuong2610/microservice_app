"""Embeddings helper built on top of LLMService."""

from typing import List
from services.llm_service import build_default_service, LLMService

class EmbeddingsClient:
    """Creates embeddings for provided texts using configured LLM service."""

    def __init__(self, service: LLMService | None = None) -> None:
        self.service = service or build_default_service()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Returns embeddings for a list of texts."""
        return self.service.embed(texts)

