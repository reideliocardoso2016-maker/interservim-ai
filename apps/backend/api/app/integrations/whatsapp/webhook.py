from fastapi import APIRouter, Request, HTTPException
from app.core.config import settings
import hashlib
import hmac
import json

router = APIRouter(prefix="/webhooks", tags=["WhatsApp Webhook"])


@router.get("/whatsapp")
def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None,
):
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def receive_webhook(request: Request):
    body = await request.json()
    # Process incoming WhatsApp messages
    if "entry" in body:
        for entry in body["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    for message in value["messages"]:
                        await process_incoming_message(message, value.get("metadata", {}))
    return {"status": "ok"}


async def process_incoming_message(message: dict, metadata: dict):
    from app.core.database import SessionLocal
    from app.models.customer import Customer
    from app.models.conversation import Conversation, Message as MessageModel
    from app.models.product import Product
    from app.core.enums import Channel, ConversationStatus, MessageSenderType, MessageType
    from datetime import datetime, timezone

    db = SessionLocal()
    try:
        phone = message.get("from", "")
        msg_text = message.get("text", {}).get("body", "")
        msg_id = message.get("id", "")
        msg_type = message.get("type", "text")
        # Find or create customer
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        if not customer:
            customer = Customer(name=phone, phone=phone, status="NEW")
            db.add(customer)
            db.flush()
        # Find or create conversation
        conversation = db.query(Conversation).filter(
            Conversation.customer_id == customer.id,
            Conversation.channel == Channel.WHATSAPP,
            Conversation.status.in_([ConversationStatus.ACTIVE, ConversationStatus.HUMAN_HANDOFF]),
        ).first()
        if not conversation:
            conversation = Conversation(
                customer_id=customer.id,
                channel=Channel.WHATSAPP,
            )
            db.add(conversation)
            db.flush()
        # Save incoming message
        msg = MessageModel(
            conversation_id=conversation.id,
            sender_type=MessageSenderType.CUSTOMER,
            content=msg_text,
            message_type=MessageType.TEXT,
            external_message_id=msg_id,
        )
        db.add(msg)
        customer.last_contacted_at = datetime.now(timezone.utc)
        db.commit()
        # If AI is enabled, generate auto-response
        if conversation.ai_enabled and conversation.status != ConversationStatus.HUMAN_HANDOFF:
            await generate_ai_response(db, conversation, customer, msg_text)
    finally:
        db.close()


async def generate_ai_response(db, conversation, customer, customer_message: str):
    from app.ai.router import get_ai_provider
    from app.models.message import Message as MessageModel
    from app.core.enums import MessageSenderType
    from datetime import datetime, timezone
    messages = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation.id
    ).order_by(MessageModel.created_at.desc()).limit(10).all()
    messages.reverse()
    context = [
        {"role": "user" if m.sender_type == "CUSTOMER" else "assistant", "content": m.content}
        for m in messages
    ]
    products = db.query(Product).filter(Product.is_active == True, Product.availability_status == "AVAILABLE").limit(10).all()
    product_context = "\n".join([f"- {p.name} (${p.unit_price}) - Origen: {p.origin_country or 'N/A'}" for p in products])
    system_prompt = f"""Eres el agente comercial virtual de InterServim-SL.

Cliente: {customer.name}
País: {customer.country or 'No especificado'}
Etapa de venta: {conversation.sales_stage}

Productos disponibles:
{product_context}

REGLAS:
- No inventes información sobre productos, precios o disponibilidad
- Usa SOLO los productos listados arriba
- Sé natural, profesional y cercano
- Avanza la conversación hacia una acción comercial"""
    try:
        provider = await get_ai_provider()
        response_text = await provider.generate_response(system_prompt, context)
        ai_msg = MessageModel(
            conversation_id=conversation.id,
            sender_type=MessageSenderType.AI_AGENT,
            content=response_text,
        )
        db.add(ai_msg)
        conversation.updated_at = datetime.now(timezone.utc)
        db.commit()
    except Exception as e:
        print(f"AI response error: {e}")
