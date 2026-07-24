from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.core.enums import UserRole


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.SALES_AGENT


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    sku: Optional[str] = None
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    origin_country: Optional[str] = None
    unit_price: float
    currency: str = "USD"
    minimum_order_quantity: int = 1
    packaging: Optional[str] = None
    availability_status: str = "AVAILABLE"
    container_capacity: Optional[str] = None
    technical_information: Optional[dict] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    origin_country: Optional[str] = None
    unit_price: Optional[float] = None
    currency: Optional[str] = None
    minimum_order_quantity: Optional[int] = None
    packaging: Optional[str] = None
    availability_status: Optional[str] = None
    container_capacity: Optional[str] = None
    technical_information: Optional[dict] = None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    sku: Optional[str]
    category_id: Optional[UUID]
    description: Optional[str]
    brand: Optional[str]
    origin_country: Optional[str]
    unit_price: float
    currency: str
    minimum_order_quantity: int
    packaging: Optional[str]
    availability_status: str
    container_capacity: Optional[str]
    technical_information: Optional[dict]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    customer_type: Optional[str] = None
    notes: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    customer_type: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class CustomerResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    email: Optional[str]
    country: Optional[str]
    company: Optional[str]
    customer_type: Optional[str]
    status: str
    notes: Optional[str]
    last_contacted_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    customer_id: UUID
    channel: str = "WHATSAPP"


class ConversationResponse(BaseModel):
    id: UUID
    customer_id: UUID
    channel: str
    status: str
    assigned_user_id: Optional[UUID]
    ai_enabled: bool
    sales_stage: str
    ai_context_summary: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str
    sender_type: str = "HUMAN_AGENT"
    message_type: str = "TEXT"


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_type: str
    content: str
    message_type: str
    intent: Optional[str]
    external_message_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class QuoteCreate(BaseModel):
    customer_id: UUID
    currency: str = "USD"
    destination_country: Optional[str] = None
    destination_port: Optional[str] = None
    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None
    valid_until: Optional[str] = None
    notes: Optional[str] = None
    items: list


class QuoteItemCreate(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: float


class QuoteResponse(BaseModel):
    id: UUID
    customer_id: UUID
    quote_number: str
    status: str
    currency: str
    total: float
    destination_country: Optional[str]
    destination_port: Optional[str]
    valid_until: Optional[str]
    notes: Optional[str]
    pdf_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class FollowUpCreate(BaseModel):
    customer_id: UUID
    conversation_id: Optional[UUID] = None
    scheduled_at: str
    message: str


class FollowUpResponse(BaseModel):
    id: UUID
    customer_id: UUID
    conversation_id: Optional[UUID]
    type: str
    scheduled_at: datetime
    status: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class MarketingCampaignCreate(BaseModel):
    name: str
    objective: str
    target_audience: Optional[str] = None


class MarketingCampaignResponse(BaseModel):
    id: UUID
    name: str
    objective: str
    target_audience: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MarketingGenerateRequest(BaseModel):
    product_id: Optional[UUID] = None
    content_type: str = "WHATSAPP_STATUS"
    objective: str = "PROMOTE_PRODUCT"
    tone: str = "PROFESSIONAL"
    language: str = "ES"
    audience: Optional[str] = None


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int


class PaginatedResponse(BaseModel):
    success: bool = True
    data: list
    meta: PaginationMeta
