from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Chat(BaseModel):
    chat_id: str
    user_id: str
    title: str
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ChatCreate(BaseModel):
    title: str = "New Chat"

class MessageCreate(BaseModel):
    content: str
