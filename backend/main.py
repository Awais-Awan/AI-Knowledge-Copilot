from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title = settings.APP_NAME,
    version = "0.1.0"
)

@app.get("/health")
def health_check():
    return {"status":"OK",
            "Enviornment": settings.ENV}

