import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum as SAEnum, ForeignKey
from app.core.database import Base, UUID_TYPE
from app.core.enums import ConversationStatus, SalesStage, Channel, MessageSenderType, MessageType, Intent


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID_TYPE, ForeignKey("customers.id"), nullable=False, index=True)
    channel = Column(SAEnum(Channel), nullable=False)
    status = Column(SAEnum(ConversationStatus), nullable=False, default=ConversationStatus.ACTIVE)
    assigned_user_id = Column(UUID_TYPE, ForeignKey("users.id"), nullable=True, index=True)
    ai_enabled = Column(Boolean, default=True)
    sales_stage = Column(SAEnum(SalesStage), nullable=False, default=SalesStage.LEAD)
    ai_context_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID_TYPE, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_type = Column(SAEnum(MessageSenderType), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(SAEnum(MessageType), default=MessageType.TEXT)
    intent = Column(SAEnum(Intent), nullable=True)
    external_message_id = Column(String(255), nullable=True)
    external_metadata = Column("metadata", Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
