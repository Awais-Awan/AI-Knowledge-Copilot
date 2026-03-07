from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.document import DocumentCreate, DocumentSearch
from app.services.document_service import create_document_with_chunks
from sqlalchemy import text
from app.services.embedding_service import generate_embedding

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/")
def upload_document(
    payload: DocumentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    document = create_document_with_chunks(
        db=db,
        title=payload.title,
        content=payload.content,
        owner_id=current_user.id
    )

    return {
        "message": "Document stored with chunks",
        "document_id": document.id
    }




@router.post("/search")
def search_documents(
    payload: DocumentSearch,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    query_embedding = generate_embedding(payload.query)

    sql = text("""
    SELECT dc.content,
           d.title,
           dc.embedding <=> CAST(:query_embedding AS vector) AS distance
    FROM document_chunks dc
    JOIN documents d ON dc.document_id = d.id
    WHERE d.owner_id = :owner_id
    ORDER BY dc.embedding <=> CAST(:query_embedding AS vector)
    LIMIT :top_k
    """)

    results = db.execute(
        sql,
        {
            "query_embedding": query_embedding,
            "owner_id": current_user.id,
            "top_k": payload.top_k
        }
    ).mappings().all()

    return {"results": results}