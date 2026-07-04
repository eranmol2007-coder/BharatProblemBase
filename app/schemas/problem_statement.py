from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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


class ProblemStatementResponse(ProblemStatementBase):
    id: int
    submission_deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    items: list[ProblemStatementResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
