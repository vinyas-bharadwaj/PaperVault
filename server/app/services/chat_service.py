from ..config import client as genai_client
from ..database import chats_collection
from ..schemas import Chat, Message
from .rag_service import rag_service
from datetime import datetime
from typing import List, Optional
import uuid

class ChatService:
    @staticmethod
    def create_chat(user_id: str, title: str = "New Chat") -> Chat:
        """Create a new chat conversation"""
        chat_id = str(uuid.uuid4())
        chat_data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "title": title,
            "messages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        chats_collection.insert_one(chat_data)
        return Chat(**chat_data)
    
    @staticmethod
    def get_chat(chat_id: str, user_id: str) -> Optional[Chat]:
        """Get a specific chat by ID"""
        chat_data = chats_collection.find_one({"chat_id": chat_id, "user_id": user_id})
        if chat_data:
            chat_data.pop("_id", None)
            return Chat(**chat_data)
        return None
    
    @staticmethod
    def list_user_chats(user_id: str, limit: int = 50, skip: int = 0) -> List[Chat]:
        """List all chats for a user"""
        chats = chats_collection.find(
            {"user_id": user_id}
        ).sort("updated_at", -1).skip(skip).limit(limit)
        
        result = []
        for chat_data in chats:
            chat_data.pop("_id", None)
            result.append(Chat(**chat_data))
        return result
    
    @staticmethod
    def delete_chat(chat_id: str, user_id: str) -> bool:
        """Delete a chat"""
        result = chats_collection.delete_one({"chat_id": chat_id, "user_id": user_id})
        return result.deleted_count > 0
    
    @staticmethod
    def add_message(chat_id: str, user_id: str, role: str, content: str) -> Optional[Message]:
        """Add a message to a chat"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        
        result = chats_collection.update_one(
            {"chat_id": chat_id, "user_id": user_id},
            {
                "$push": {"messages": message},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.modified_count > 0:
            return Message(**message)
        return None
    
    @staticmethod
    def generate_response(messages: List[Message], use_rag: bool = True) -> str:
        """Generate AI response using Gemini with optional RAG"""
        # Get the latest user message for RAG context
        latest_message = messages[-1].content if messages else ""
        
        if use_rag:
            # Use RAG pipeline for context-aware responses
            # Convert message history to conversation format
            conversation_history = []
            for msg in messages[:-1]:  # Exclude the latest message (already used in RAG query)
                role = "user" if msg.role == "user" else "model"
                conversation_history.append({"role": role, "parts": [{"text": msg.content}]})
            
            # Generate RAG response
            return rag_service.generate_rag_response(latest_message, conversation_history)
        else:
            # Standard conversation without RAG
            conversation = []
            for msg in messages:
                role = "user" if msg.role == "user" else "model"
                conversation.append({"role": role, "parts": [{"text": msg.content}]})
            
            # Generate response
            response = genai_client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=conversation
            )
            
            return response.text
    
    @staticmethod
    async def send_message(chat_id: str, user_id: str, user_message: str) -> dict:
        """Send a message and get AI response"""
        # Get chat
        chat = ChatService.get_chat(chat_id, user_id)
        if not chat:
            return {"error": "Chat not found"}
        
        # Add user message
        user_msg = ChatService.add_message(chat_id, user_id, "user", user_message)
        if not user_msg:
            return {"error": "Failed to add message"}
        
        # Get all messages for context
        updated_chat = ChatService.get_chat(chat_id, user_id)
        
        # Generate AI response
        ai_response = ChatService.generate_response(updated_chat.messages)
        
        # Add AI response to chat
        ai_msg = ChatService.add_message(chat_id, user_id, "assistant", ai_response)
        
        return {
            "user_message": user_msg,
            "assistant_message": ai_msg
        }

chat_service = ChatService()
