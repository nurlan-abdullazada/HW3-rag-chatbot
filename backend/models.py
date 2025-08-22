from typing import Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"


class ChatResponse(BaseModel):
    response: str
    status: str = "success"


class HealthResponse(BaseModel):
    status: str
    message: str
