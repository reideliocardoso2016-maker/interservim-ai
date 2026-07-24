from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.customer import Customer
from app.models.conversation import Conversation, Message
from app.models.quote import Quote
from app.models.product import Product
from app.core.enums import UserRole
from fastapi import HTTPException

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    total_customers = db.query(Customer).filter(Customer.deleted_at.is_(None)).count()
    active_conversations = db.query(Conversation).filter(Conversation.status == "ACTIVE").count()
    open_opportunities = db.query(Conversation).filter(
        Conversation.sales_stage.in_(["QUALIFIED", "PRODUCT_INTEREST", "QUOTE_REQUESTED", "QUOTE_SENT", "NEGOTIATION"])
    ).count()
    total_quotes = db.query(Quote).count()
    won_quotes = db.query(Quote).filter(Quote.status == "ACCEPTED").count()
    total_messages = db.query(Message).count()
    return {
        "success": True,
        "data": {
            "total_customers": total_customers,
            "active_conversations": active_conversations,
            "open_opportunities": open_opportunities,
            "total_quotes": total_quotes,
            "won_quotes": won_quotes,
            "total_messages": total_messages,
            "conversion_rate": round((won_quotes / total_quotes * 100) if total_quotes > 0 else 0, 2),
        },
    }


@router.get("/conversations")
def get_conversation_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    stages = db.query(Conversation.sales_stage, func.count(Conversation.id)).group_by(Conversation.sales_stage).all()
    return {"success": True, "data": {stage: count for stage, count in stages}}


@router.get("/products")
def get_product_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    from app.models.quote import QuoteItem
    products = db.query(
        Product.name, Product.sku, func.count(QuoteItem.id).label("times_quoted")
    ).outerjoin(QuoteItem, QuoteItem.product_id == Product.id
    ).group_by(Product.id, Product.name, Product.sku
    ).order_by(func.count(QuoteItem.id).desc()).limit(20).all()
    return {"success": True, "data": [{"name": p.name, "sku": p.sku, "times_quoted": p.times_quoted} for p in products]}
