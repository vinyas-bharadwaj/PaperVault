from qdrant_client.models import PointStruct
from ..config import qdrant

class VectorService:
    def __init__(self):
        self.collection_name = "papers"
    
    def store_document(self, doc_id: str, embedding: list[float], metadata: dict) -> None:
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
    
    def list_all_documents(self, limit: int = 10, offset: int = 0) -> list:
        """List all documents with pagination"""
        results = qdrant.scroll(
            collection_name=self.collection_name,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        return results[0]  # scroll returns (points, next_page_offset)
    
    def get_document_count(self) -> int:
        """Get total count of documents in collection"""
        collection_info = qdrant.get_collection(collection_name=self.collection_name)
        return collection_info.points_count
    
    def get_document_by_id(self, doc_id: str):
        """Retrieve a specific document by ID"""
        try:
            result = qdrant.retrieve(
                collection_name=self.collection_name,
                ids=[doc_id],
                with_payload=True,
                with_vectors=False
            )
            return result[0] if result else None
        except Exception:
            return None

vector_service = VectorService()
