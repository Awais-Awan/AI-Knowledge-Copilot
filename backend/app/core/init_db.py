from app.core.database import engine, Base

from app.models.user import User

def init():
    # Base.metadata.create_all(bind=engine)    #"Database initialization now handled by Alembic."
    pass

if __name__ == "__main__":
    init()