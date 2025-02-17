from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base

DATABASE_URL = "postgresql://postgres:root@localhost/signetic_ai_scheduler"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    try:
        Base.metadata.create_all(bind=engine)  # Create tables
    except Exception as e:
        print(f"Error initializing database: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 