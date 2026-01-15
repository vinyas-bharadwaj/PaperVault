from ..config import client

class EmbeddingService:
    def __init__(self):
        self.model = "text-embedding-004"
    
    def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector for given text"""
        response = client.models.embed_content(
            model=self.model,
            contents=[text]
        )
        return response.embeddings[0].values

embedding_service = EmbeddingService()
