from app.core.database import engine, Base

from app.models import user  

def init():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init()