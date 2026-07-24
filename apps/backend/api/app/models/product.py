import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import UUID_TYPE
from app.core.database import Base
from app.core.enums import AvailabilityStatus


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(UUID_TYPE, ForeignKey("product_categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, nullable=True, index=True)
    category_id = Column(UUID_TYPE, ForeignKey("product_categories.id"), nullable=True)
    description = Column(Text, nullable=True)
    brand = Column(String(255), nullable=True)
    origin_country = Column(String(100), nullable=True)
    unit_price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD")
    minimum_order_quantity = Column(Integer, default=1)
    packaging = Column(String(255), nullable=True)
    availability_status = Column(SAEnum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE)
    container_capacity = Column(String(100), nullable=True)
    technical_information = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID_TYPE, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=False)
    type = Column(String(50), default="PRIMARY")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
