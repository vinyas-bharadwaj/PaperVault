from typing import List, Dict
from .embedding_service import embedding_service
from .vector_service import vector_service
from ..config import client as genai_client

class RAGService:
    """Retrieval Augmented Generation service for context-aware chat responses"""
    
    def __init__(self):
        self.top_k = 3  # Number of documents to retrieve
        self.model = "gemini-2.5-flash"
    
    def retrieve_context(self, query: str) -> List[Dict]:
        """Retrieve relevant document chunks based on query"""
        # Generate embedding for the query
        query_embedding = embedding_service.generate_embedding(query)
        
        # Search for similar documents
        results = vector_service.search_similar(query_embedding, limit=self.top_k)
        
        # Extract relevant information including all metadata
        context_docs = []
        for point in results:
            context_docs.append({
                "title": point.payload.get("title", "Untitled"),
                "text": point.payload.get("text", ""),
                "professor": point.payload.get("professor", "Unknown"),
                "subject": point.payload.get("subject", "N/A"),
                "semester": point.payload.get("semester", "N/A"),
                "filename": point.payload.get("filename", "N/A"),
                "score": point.score
            })
        
        return context_docs
    
    def format_context(self, context_docs: List[Dict]) -> str:
        """Format retrieved documents into a context string"""
        if not context_docs:
            return ""
        
        context_parts = ["Here are some relevant documents from your knowledge base:\n"]
        
        for i, doc in enumerate(context_docs, 1):
            context_parts.append(f"\n--- Document {i} ---")
            context_parts.append(f"Title: {doc['title']}")
            context_parts.append(f"Professor: {doc['professor']}")
            context_parts.append(f"Subject: {doc['subject']}")
            context_parts.append(f"Semester: {doc['semester']}")
            context_parts.append(f"\nContent:\n{doc['text'][:1000]}")  # Limit text length
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def generate_rag_response(self, user_query: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using RAG pipeline"""
        # Step 1: Retrieve relevant context
        context_docs = self.retrieve_context(user_query)
        
        # Step 2: Format context
        context = self.format_context(context_docs)
        
        # Step 3: Build prompt with context
        if context:
            system_prompt = f"""You are a helpful AI assistant with access to a knowledge base of documents. 
Use the provided context to answer the user's question accurately. If the context doesn't contain 
relevant information, you can still provide a helpful response based on your general knowledge, 
but mention that the information is not from the knowledge base.

{context}
"""
        else:
            system_prompt = "You are a helpful AI assistant."
        
        # Step 4: Prepare conversation with context
        messages = []
        
        # Add system context as first message
        if context:
            messages.append({"role": "user", "parts": [{"text": system_prompt}]})
            messages.append({"role": "model", "parts": [{"text": "I understand. I'll use the provided documents to answer your questions accurately."}]})
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current query
        messages.append({"role": "user", "parts": [{"text": user_query}]})
        
        # Step 5: Generate response
        response = genai_client.models.generate_content(
            model=self.model,
            contents=messages
        )
        
        return response.text

rag_service = RAGService()
