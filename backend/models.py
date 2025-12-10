from typing import List
from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    filename: str
    pages: int
    chunks: int


class QuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    text: str
    page: int
    chunk_id: int


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]


class HealthResponse(BaseModel):
    status: str
    documents_count: int
    model: str
