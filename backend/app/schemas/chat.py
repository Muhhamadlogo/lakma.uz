from typing import Any

from pydantic import BaseModel

from app.schemas.product import ProductRead


class ChatRequest(BaseModel):
    user_id: int
    message: str


class ArtifactRead(BaseModel):
    artifact_type: str
    content_json: dict[str, Any]


class ChatResponse(BaseModel):
    intent: str
    agent: str
    reply: str
    products: list[ProductRead]
    artifacts: list[ArtifactRead]
    run_id: int
