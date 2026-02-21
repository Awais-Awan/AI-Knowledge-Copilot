from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.embedding_service import generate_embedding
from app.schemas.document import DocumentCreate
from app.models.documents import Document

router = APIRouter(prefix= "/documents", tags=["Documents"])

@router.post("/")
def upload_document(
    payload : DocumentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    embedding = generate_embedding(payload.content)
    

    document = Document(
        title = payload.title,
        content = payload.content,
        embedding = embedding,
        owner_id = current_user.id,
    )

    db.add(document)
    db.commit(document)
    db.refresh(document)

    return {"message": "Stored with open-source embeddings"}