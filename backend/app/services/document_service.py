from sqlalchemy.orm import Session
from app.models.documents import Document
from app.models.document_chunk import DocumentChunk
from app.utils.chunking import chunk_text
from app.services.embedding_service import generate_embedding


def create_document_with_chunks(
    db: Session,
    title: str,
    content: str,
    owner_id: int
):

    # save document
    document = Document(
        title=title,
        content=content,
        owner_id=owner_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # split text
    chunks = chunk_text(content)

    # create chunk rows
    for chunk in chunks:

        embedding = generate_embedding(chunk)

        chunk_row = DocumentChunk(
            document_id=document.id,
            content=chunk,
            embedding=embedding
        )

        db.add(chunk_row)

    db.commit()

    return document