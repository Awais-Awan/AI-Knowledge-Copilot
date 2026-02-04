from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/only")
def admin_only_route(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    return {"message": "Welcome admin"}
