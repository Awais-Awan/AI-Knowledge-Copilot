from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password
from app.core.jwt import create_access_token
from fastapi import HTTPException
from app.core.security import hash_password

def authenticate_user(db: Session,email :str, password :str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    token = create_access_token(
        subject= str(user.id),
        role= user.role
    )

    return token


def register_user(db: Session, email: str, password: str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role="admin"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
  
