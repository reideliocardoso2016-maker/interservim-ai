from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.marketing import MarketingCampaign, MarketingContent
from app.schemas.schemas import MarketingCampaignCreate, MarketingCampaignResponse
from app.core.enums import UserRole
import uuid

router = APIRouter(prefix="/marketing", tags=["Marketing AI Studio"])


@router.get("/campaigns")
def list_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaigns = db.query(MarketingCampaign).order_by(MarketingCampaign.created_at.desc()).all()
    return {"success": True, "data": [MarketingCampaignResponse.model_validate(c) for c in campaigns]}


@router.post("/campaigns", response_model=MarketingCampaignResponse)
def create_campaign(
    data: MarketingCampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    campaign = MarketingCampaign(
        name=data.name,
        objective=data.objective,
        target_audience=data.target_audience,
        created_by=current_user.id,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("/campaigns/{campaign_id}")
def get_campaign(
    campaign_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    contents = db.query(MarketingContent).filter(MarketingContent.campaign_id == campaign_id).all()
    return {
        "success": True,
        "data": {
            **MarketingCampaignResponse.model_validate(campaign).model_dump(),
            "contents": [{"id": str(c.id), "content_type": c.content_type, "title": c.title, "body": c.body} for c in contents],
        },
    }


@router.post("/campaigns/{campaign_id}/generate")
async def generate_content(
    campaign_id: str,
    params: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    campaign = db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    from app.ai.router import get_ai_provider
    provider = await get_ai_provider()
    result = await provider.generate_marketing_content(params)
    content = MarketingContent(
        campaign_id=campaign_id,
        content_type=params.get("content_type", "WHATSAPP_STATUS"),
        body=result.get("content", ""),
        tone=params.get("tone", "PROFESSIONAL"),
        language=params.get("language", "ES"),
        ai_generated=True,
    )
    db.add(content)
    db.commit()
    return {"success": True, "data": result}
