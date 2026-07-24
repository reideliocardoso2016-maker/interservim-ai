from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk
from app.core.enums import UserRole, DocumentType
import os
import uuid

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    ext = file.filename.split(".")[-1].upper() if "." in file.filename else "TXT"
    if ext not in ["PDF", "DOCX", "XLSX", "TXT"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    file_id = str(uuid.uuid4())
    file_path = os.path.join(upload_dir, f"{file_id}_{file.filename}")
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    doc = KnowledgeDocument(
        name=file.filename,
        file_url=file_path,
        document_type=ext,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"success": True, "document_id": str(doc.id), "name": doc.name}


@router.get("/documents")
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    docs = db.query(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc()).all()
    return {"success": True, "data": [{"id": str(d.id), "name": d.name, "type": d.document_type, "status": d.status, "created_at": d.created_at.isoformat()} for d in docs]}


@router.delete("/documents/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if os.path.exists(doc.file_url):
        os.remove(doc.file_url)
    db.query(KnowledgeChunk).filter(KnowledgeChunk.document_id == document_id).delete()
    db.delete(doc)
    db.commit()
    return {"success": True}


@router.get("/search")
def search_knowledge(
    query: str = Query(...),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chunks = db.query(KnowledgeChunk).filter(
        KnowledgeChunk.content.ilike(f"%{query}%")
    ).limit(limit).all()
    return {"success": True, "data": [{"content": c.content, "document_id": str(c.document_id)} for c in chunks]}
