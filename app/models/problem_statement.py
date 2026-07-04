from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func

from app.database import Base


class ProblemStatement(Base):
    __tablename__ = "problem_statements"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=False)

    domain = Column(String(100), index=True)
    organization = Column(String(200), index=True)
    category = Column(String(100), index=True)
    source_platform = Column(String(100), index=True, default="general")

    source_year = Column(Integer, index=True)
    source_link = Column(String(1000))

    tags = Column(JSON, default=list)
    difficulty = Column(String(50))

    submission_deadline = Column(DateTime, nullable=True)
    is_open = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<ProblemStatement id={self.id} title='{self.title[:40]}...'>"
