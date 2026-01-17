from fastapi import APIRouter, Depends, HTTPException, Query
from ..schemas import Chat, ChatCreate, MessageCreate, Message
from ..services.chat_service import chat_service
from ..routers.auth import get_current_user
from typing import List

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=Chat)
async def create_chat(
    chat_data: ChatCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new chat conversation"""
    chat = chat_service.create_chat(
        user_id=current_user["email"],
        title=chat_data.title
    )
    return chat

@router.get("/", response_model=List[Chat])
async def list_chats(
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
    current_user: dict = Depends(get_current_user)
):
    """List all chats for the current user"""
    chats = chat_service.list_user_chats(
        user_id=current_user["email"],
        limit=limit,
        skip=skip
    )
    return chats

@router.get("/{chat_id}", response_model=Chat)
async def get_chat(
    chat_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific chat by ID"""
    chat = chat_service.get_chat(chat_id, current_user["email"])
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a chat"""
    success = chat_service.delete_chat(chat_id, current_user["email"])
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}

@router.post("/{chat_id}/message")
async def send_message(
    chat_id: str,
    message: MessageCreate,
    current_user: dict = Depends(get_current_user)
):
    """Send a message to a chat and get AI response"""
    result = await chat_service.send_message(
        chat_id=chat_id,
        user_id=current_user["email"],
        user_message=message.content
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/{chat_id}/messages", response_model=List[Message])
async def get_messages(
    chat_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all messages from a chat"""
    chat = chat_service.get_chat(chat_id, current_user["email"])
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat.messages
