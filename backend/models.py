from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

class HealthResponse(BaseModel):
    status: str
    message: str
