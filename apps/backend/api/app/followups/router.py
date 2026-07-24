from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.followup import FollowUp
from app.models.customer import Customer
from app.schemas.schemas import FollowUpCreate, FollowUpResponse
from datetime import datetime, timezone
import math

router = APIRouter(prefix="/followups", tags=["Follow-Ups"])


@router.get("")
def list_followups(
    status_filter: str = Query(None, alias="status"),
    customer_id: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(FollowUp)
    if status_filter:
        query = query.filter(FollowUp.status == status_filter)
    if customer_id:
        query = query.filter(FollowUp.customer_id == customer_id)
    total = query.count()
    pages = math.ceil(total / per_page)
    followups = query.order_by(FollowUp.scheduled_at).offset((page - 1) * per_page).limit(per_page).all()
    return {
        "success": True,
        "data": [FollowUpResponse.model_validate(f) for f in followups],
        "meta": {"page": page, "per_page": per_page, "total": total, "pages": pages},
    }


@router.post("")
def create_followup(
    data: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    followup = FollowUp(
        customer_id=data.customer_id,
        conversation_id=data.conversation_id,
        type="MANUAL",
        message=data.message,
        scheduled_at=datetime.fromisoformat(data.scheduled_at) if isinstance(data.scheduled_at, str) else data.scheduled_at,
    )
    db.add(followup)
    db.commit()
    db.refresh(followup)
    return {"success": True, "data": FollowUpResponse.model_validate(followup)}


@router.patch("/{followup_id}")
def update_followup(
    followup_id: str,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    followup = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    followup.status = status
    if status == "SENT":
        followup.executed_at = datetime.now(timezone.utc)
    db.commit()
    return {"success": True}
