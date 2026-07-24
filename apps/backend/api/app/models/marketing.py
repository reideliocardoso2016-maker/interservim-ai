import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer
from app.core.database import Base, UUID_TYPE
from app.core.enums import CampaignObjective, ContentType


class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    objective = Column(SAEnum(CampaignObjective), nullable=False)
    target_audience = Column(String(500), nullable=True)
    status = Column(String(50), default="DRAFT")
    created_by = Column(UUID_TYPE, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class MarketingContent(Base):
    __tablename__ = "marketing_contents"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID_TYPE, ForeignKey("marketing_campaigns.id"), nullable=False)
    content_type = Column(SAEnum(ContentType), nullable=False)
    language = Column(String(10), default="ES")
    title = Column(String(500), nullable=True)
    body = Column(Text, nullable=False)
    call_to_action = Column(String(255), nullable=True)
    media_url = Column(String(500), nullable=True)
    tone = Column(String(50), default="PROFESSIONAL")
    ai_generated = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
