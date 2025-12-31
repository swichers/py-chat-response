from pydantic import BaseModel
from typing import List


class CreateContextRequest(BaseModel):
    name: str
    content: str


class CreateContextResponse(BaseModel):
    machine_name: str
    message: str


class ContextInfo(BaseModel):
    machine_name: str
    file_path: str


class ListContextsResponse(BaseModel):
    contexts: List[ContextInfo]


class DeleteContextResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
