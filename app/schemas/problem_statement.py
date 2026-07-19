import json
from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import datetime


def _parse_tags(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return [str(t) for t in parsed]
            return [str(parsed)]
        except (json.JSONDecodeError, TypeError):
            return [v]
    return []


class ProblemStatementBase(BaseModel):
    title: str
    description: str
    domain: Optional[str] = None
    organization: Optional[str] = None
    category: Optional[str] = None
    source_platform: Optional[str] = "general"
    source_year: Optional[int] = None
    source_link: Optional[str] = None
    tags: Optional[list[str]] = []
    difficulty: Optional[str] = None
    is_open: Optional[bool] = True

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v: Any) -> list[str]:
        return _parse_tags(v)


class ProblemStatementCreate(ProblemStatementBase):
    pass


class ProblemStatementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    organization: Optional[str] = None
    category: Optional[str] = None
    source_platform: Optional[str] = None
    source_year: Optional[int] = None
    source_link: Optional[str] = None
    tags: Optional[list[str]] = None
    difficulty: Optional[str] = None
    is_open: Optional[bool] = None

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v: Any) -> Optional[list[str]]:
        if v is None:
            return None
        return _parse_tags(v)


class ProblemStatementResponse(ProblemStatementBase):
    id: int
    submission_deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: Optional[list[str]] = []

    model_config = {"from_attributes": True}

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v: Any) -> list[str]:
        return _parse_tags(v)

    @field_validator("description", mode="before")
    @classmethod
    def ensure_description(cls, v: Any) -> str:
        if v is None:
            return ""
        return str(v)


class PaginatedResponse(BaseModel):
    items: list[ProblemStatementResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
