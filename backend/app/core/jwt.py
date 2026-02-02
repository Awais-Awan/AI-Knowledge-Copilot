from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(subject :str, role :str, expire_time :int = 60):
    expire = datetime.now() + timedelta(minutes=expire_time)

    payload = {
        "sub":subject,
        "role":role,
        "exp":expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm= ALGORITHM
    )
