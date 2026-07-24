from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.models.product import Product
from app.models.customer import Customer
from app.core.enums import Intent, MessageSenderType, SalesStage
from app.core.config import settings
from datetime import datetime, timezone
import json

router = APIRouter(prefix="/ai", tags=["AI"])


async def get_ai_provider():
    provider_name = settings.ai_provider
    if provider_name == "openai":
        from app.ai.openai_provider import OpenAIProvider
        return OpenAIProvider(api_key=settings.ai_api_key, model=settings.ai_model)
    raise HTTPException(status_code=500, detail=f"AI provider '{provider_name}' not configured")


@router.post("/classify")
async def classify_intent(
    message: str,
    context: str = "",
    current_user: User = Depends(get_current_user),
):
    provider = await get_ai_provider()
    intent = await provider.classify_intent(message, context)
    return {"success": True, "intent": intent}


@router.post("/generate")
async def generate_response(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    customer = db.query(Customer).filter(Customer.id == conversation.customer_id).first()
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).limit(10).all()
    messages.reverse()
    context_messages = [
        {"role": "user" if m.sender_type == "CUSTOMER" else "assistant", "content": m.content}
        for m in messages
    ]
    customer_context = f"Cliente: {customer.name}\nPaís: {customer.country or 'No especificado'}\nEmpresa: {customer.company or 'No especificada'}\nTipo: {customer.customer_type or 'No especificado'}\nEstado: {customer.status}"
    product_context = "Productos disponibles en catálogo:\n"
    products = db.query(Product).filter(Product.is_active == True, Product.availability_status == "AVAILABLE").limit(10).all()
    for p in products:
        product_context += f"- {p.name} (SKU: {p.sku}) - ${p.unit_price} {p.currency} - Origen: {p.origin_country or 'N/A'}\n"
    system_prompt = f"""Eres el agente comercial virtual de InterServim-SL.

INFORMACIÓN DEL CLIENTE:
{customer_context}

CATÁLOGO DISPONIBLE:
{product_context}

ETAPA DE VENTA ACTUAL: {conversation.sales_stage}

Debes actuar como un vendedor profesional. No inventes información. Usa solo los productos listados arriba."""
    provider = await get_ai_provider()
    response_text = await provider.generate_response(system_prompt, context_messages)
    ai_message = Message(
        conversation_id=conversation_id,
        sender_type=MessageSenderType.AI_AGENT,
        content=response_text,
    )
    db.add(ai_message)
    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ai_message)
    return {"success": True, "response": response_text, "message_id": str(ai_message.id)}


@router.post("/marketing")
async def generate_marketing_content(
    params: dict,
    current_user: User = Depends(get_current_user),
):
    provider = await get_ai_provider()
    result = await provider.generate_marketing_content(params)
    return {"success": True, "data": result}
