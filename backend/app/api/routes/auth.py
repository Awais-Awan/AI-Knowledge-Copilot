from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest, UserResponse
from app.services.auth_service import authenticate_user,register_user
from app.core.database import get_db

router = APIRouter(prefix = "/auth", tags = ["Auth"])

@router.post("/login", response_model = TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = authenticate_user(db, data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail = "Invalid Credentials")
    return {"access_token": token}



@router.post("/register", response_model=UserResponse)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    return register_user(db, data.email, data.password)
