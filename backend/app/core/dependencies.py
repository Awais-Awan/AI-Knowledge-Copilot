from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from app.core.config import settings

# OAuth2 token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Pydantic model for current user
class User(BaseModel):
    id: int
    role: str

# Dependency to get the current user from JWT
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user information"
            )

        return User(id=int(user_id), role=role)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )