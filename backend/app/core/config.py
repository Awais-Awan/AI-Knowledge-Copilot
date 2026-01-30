from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    ENV: str
    SECRET_KEY:str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()