from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.quote import Quote, QuoteItem
from app.models.product import Product
from app.models.customer import Customer
from app.schemas.schemas import QuoteCreate, QuoteResponse, PaginatedResponse, PaginationMeta
from app.core.enums import UserRole
from datetime import datetime, timezone, date
import math
import uuid

router = APIRouter(prefix="/quotes", tags=["Quotes"])


def generate_quote_number(db: Session) -> str:
    today = date.today()
    count = db.query(Quote).filter(
        Quote.created_at >= datetime(today.year, today.month, today.day, tzinfo=timezone.utc)
    ).count() + 1
    return f"COT-{today.strftime('%Y%m%d')}-{count:04d}"


@router.get("", response_model=PaginatedResponse)
def list_quotes(
    customer_id: str = Query(None),
    status_filter: str = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Quote)
    if customer_id:
        query = query.filter(Quote.customer_id == customer_id)
    if status_filter:
        query = query.filter(Quote.status == status_filter)
    total = query.count()
    pages = math.ceil(total / per_page)
    quotes = query.order_by(Quote.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(
        data=[QuoteResponse.model_validate(q) for q in quotes],
        meta=PaginationMeta(page=page, per_page=per_page, total=total, pages=pages),
    )


@router.post("", response_model=QuoteResponse)
def create_quote(
    data: QuoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    quote = Quote(
        customer_id=data.customer_id,
        quote_number=generate_quote_number(db),
        currency=data.currency,
        destination_country=data.destination_country,
        destination_port=data.destination_port,
        payment_terms=data.payment_terms,
        delivery_terms=data.delivery_terms,
        notes=data.notes,
        total=0,
        created_by=current_user.id,
    )
    if data.valid_until:
        try:
            quote.valid_until = date.fromisoformat(data.valid_until)
        except ValueError:
            pass
    db.add(quote)
    db.flush()
    total = 0
    for item_data in data.items:
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        if not product:
            continue
        qty = item_data.get("quantity", 1)
        price = item_data.get("unit_price", float(product.unit_price))
        subtotal = qty * price
        total += subtotal
        item = QuoteItem(
            quote_id=quote.id,
            product_id=item_data["product_id"],
            product_name=product.name,
            sku=product.sku,
            quantity=qty,
            unit_price=price,
            subtotal=subtotal,
        )
        db.add(item)
    quote.total = total
    db.commit()
    db.refresh(quote)
    return quote


@router.get("/{quote_id}", response_model=QuoteResponse)
def get_quote(
    quote_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    return quote


@router.put("/{quote_id}", response_model=QuoteResponse)
def update_quote(
    quote_id: str,
    data: QuoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    if data.currency:
        quote.currency = data.currency
    if data.destination_country:
        quote.destination_country = data.destination_country
    if data.destination_port:
        quote.destination_port = data.destination_port
    if data.payment_terms:
        quote.payment_terms = data.payment_terms
    if data.delivery_terms:
        quote.delivery_terms = data.delivery_terms
    if data.notes:
        quote.notes = data.notes
    db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).delete()
    total = 0
    for item_data in data.items:
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        if not product:
            continue
        qty = item_data.get("quantity", 1)
        price = item_data.get("unit_price", float(product.unit_price))
        subtotal = qty * price
        total += subtotal
        item = QuoteItem(
            quote_id=quote.id,
            product_id=item_data["product_id"],
            product_name=product.name,
            sku=product.sku,
            quantity=qty,
            unit_price=price,
            subtotal=subtotal,
        )
        db.add(item)
    quote.total = total
    db.commit()
    db.refresh(quote)
    return quote


@router.delete("/{quote_id}")
def delete_quote(
    quote_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    db.query(QuoteItem).filter(QuoteItem.quote_id == quote.id).delete()
    db.delete(quote)
    db.commit()
    return {"success": True, "message": "Quote deleted"}
