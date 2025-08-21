# api > pydantic_models.py

from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List, Any

class ModelName(str, Enum):
    GPT4_1 = "gpt-4.1"
    GPT4_1_MINI = "gpt-4.1-mini"

class QueryInput(BaseModel):
    question: str
    session_id: str | None = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT4_1_MINI)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName
    intermediate_steps: List[Any] = Field(default=[], description="Details of tool usage and timings.")

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int