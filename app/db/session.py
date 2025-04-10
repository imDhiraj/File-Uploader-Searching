# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Add this to fix the import error
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
