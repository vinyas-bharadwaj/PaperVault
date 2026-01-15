from qdrant_client.models import PointStruct
from ..config import qdrant

class VectorService:
    def __init__(self):
        self.collection_name = "papers"
    
    def store_document(self, doc_id: int, embedding: list[float], metadata: dict) -> None:
        """Store document embedding and metadata in vector database"""
        point = PointStruct(
            id=doc_id,
            vector=embedding,
            payload=metadata
        )
        qdrant.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
    
    def search_similar(self, query_vector: list[float], limit: int = 5) -> list:
        """Search for similar documents using vector similarity"""
        results = qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )
        return results.points

vector_service = VectorService()
