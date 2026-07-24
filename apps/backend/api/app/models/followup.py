import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Enum as SAEnum, ForeignKey, Integer
from app.core.database import Base, UUID_TYPE
from app.core.enums import FollowUpStatus


class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID_TYPE, ForeignKey("customers.id"), nullable=False, index=True)
    conversation_id = Column(UUID_TYPE, ForeignKey("conversations.id"), nullable=True)
    type = Column(String(50), default="AUTOMATIC")
    scheduled_at = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(SAEnum(FollowUpStatus), nullable=False, default=FollowUpStatus.PENDING)
    message = Column(Text, nullable=False)
    executed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
