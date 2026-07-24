import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Enum as SAEnum, Integer
from app.core.database import Base, UUID_TYPE
from app.core.enums import DocumentType


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    document_type = Column(SAEnum(DocumentType), nullable=False)
    status = Column(String(50), default="PROCESSING")
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID_TYPE, nullable=False)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
