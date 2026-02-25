from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from sqlalchemy import text
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.embedding_service import generate_embedding
from app.schemas.document import DocumentCreate,DocumentSearch
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
    db.commit()
    db.refresh(document)

    return {"message": "Stored with open-source embeddings"}

@router.post("/search")
def search_documents(    payload : DocumentSearch,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    
    query_embedding = generate_embedding(payload.query)
    sql = text("""
    SELECT id, title, content,
           embedding <=> CAST(:query_embedding AS vector) AS distance
    FROM documents
    WHERE owner_id = :owner_id
    ORDER BY embedding <=> CAST(:query_embedding AS vector)
    LIMIT :top_k;
    """)
    
    results = db.execute(sql, {
        "query_embedding":query_embedding,
        "owner_id": current_user.id,
        "top_k": payload.top_k
    }).mappings().all()

    return {"result" : results}