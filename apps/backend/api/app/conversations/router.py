from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.models.customer import Customer
from app.schemas.schemas import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse, PaginatedResponse, PaginationMeta
from datetime import datetime, timezone
import math

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("", response_model=PaginatedResponse)
def list_conversations(
    status_filter: str = Query(None, alias="status"),
    customer_id: str = Query(None),
    assigned_user_id: str = Query(None),
    ai_enabled: bool = Query(None),
    sales_stage: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Conversation)
    if status_filter:
        query = query.filter(Conversation.status == status_filter)
    if customer_id:
        query = query.filter(Conversation.customer_id == customer_id)
    if assigned_user_id:
        query = query.filter(Conversation.assigned_user_id == assigned_user_id)
    if ai_enabled is not None:
        query = query.filter(Conversation.ai_enabled == ai_enabled)
    if sales_stage:
        query = query.filter(Conversation.sales_stage == sales_stage)
    total = query.count()
    pages = math.ceil(total / per_page)
    conversations = query.order_by(desc(Conversation.updated_at)).offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(
        data=[ConversationResponse.model_validate(c) for c in conversations],
        meta=PaginationMeta(page=page, per_page=per_page, total=total, pages=pages),
    )


@router.post("", response_model=ConversationResponse)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    conversation = Conversation(
        customer_id=data.customer_id,
        channel=data.channel,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation


@router.patch("/{conversation_id}/ai")
def toggle_ai(
    conversation_id: str,
    enabled: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["ADMIN", "MANAGER"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    conversation.ai_enabled = enabled
    db.commit()
    return {"success": True, "ai_enabled": enabled}


@router.patch("/{conversation_id}/assign")
def assign_conversation(
    conversation_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["ADMIN", "MANAGER"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    conversation.assigned_user_id = user_id
    db.commit()
    return {"success": True, "assigned_user_id": user_id}


@router.patch("/{conversation_id}/handoff")
def request_handoff(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    conversation.status = "HUMAN_HANDOFF"
    conversation.ai_enabled = False
    db.commit()
    return {"success": True, "status": "HUMAN_HANDOFF"}


@router.get("/{conversation_id}/messages", response_model=PaginatedResponse)
def list_messages(
    conversation_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    query = db.query(Message).filter(Message.conversation_id == conversation_id)
    total = query.count()
    pages = math.ceil(total / per_page)
    messages = query.order_by(Message.created_at).offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(
        data=[MessageResponse.model_validate(m) for m in messages],
        meta=PaginationMeta(page=page, per_page=per_page, total=total, pages=pages),
    )


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
def send_message(
    conversation_id: str,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    message = Message(
        conversation_id=conversation_id,
        sender_type=data.sender_type,
        content=data.content,
        message_type=data.message_type,
    )
    db.add(message)
    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(message)
    return message
