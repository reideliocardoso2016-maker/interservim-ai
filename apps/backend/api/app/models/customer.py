import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum as SAEnum, ForeignKey
from app.core.database import Base, UUID_TYPE
from app.core.enums import CustomerType, CustomerStatus


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    company = Column(String(255), nullable=True)
    customer_type = Column(SAEnum(CustomerType), nullable=True)
    status = Column(SAEnum(CustomerStatus), nullable=False, default=CustomerStatus.NEW)
    notes = Column(Text, nullable=True)
    last_contacted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
