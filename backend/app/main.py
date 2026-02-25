from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth,admin,documents

app = FastAPI(
    title = settings.APP_NAME,
    version = "0.1.0"
)

@app.get("/health")
def health_check():
    return {"status":"OK",
            "Enviornment": settings.ENV}

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(documents.router)
