from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    text: str
    context: Optional[str] = None
    system_context: Optional[str] = None


class Message(BaseModel):
    text: str


class Output(BaseModel):
    type: str
    role: str
    content: Message


class ChatResponse(BaseModel):
    output: List[Output]
