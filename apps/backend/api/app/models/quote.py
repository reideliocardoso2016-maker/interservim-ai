import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, Date
from app.core.database import Base, UUID_TYPE
from app.core.enums import QuoteStatus


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID_TYPE, ForeignKey("customers.id"), nullable=False, index=True)
    quote_number = Column(String(50), unique=True, nullable=False)
    status = Column(SAEnum(QuoteStatus), nullable=False, default=QuoteStatus.DRAFT)
    currency = Column(String(3), default="USD")
    total = Column(Numeric(14, 2), nullable=False)
    destination_country = Column(String(100), nullable=True)
    destination_port = Column(String(100), nullable=True)
    payment_terms = Column(String(255), nullable=True)
    delivery_terms = Column(String(255), nullable=True)
    valid_until = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    pdf_url = Column(String(500), nullable=True)
    created_by = Column(UUID_TYPE, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class QuoteItem(Base):
    __tablename__ = "quote_items"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    quote_id = Column(UUID_TYPE, ForeignKey("quotes.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID_TYPE, ForeignKey("products.id"), nullable=True)
    product_name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    subtotal = Column(Numeric(14, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
