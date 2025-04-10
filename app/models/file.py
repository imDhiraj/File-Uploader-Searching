from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class ResumeFile(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)            # Actual file name on disk
    original_filename = Column(String(255), nullable=False)   # Original file name by user
    upload_time = Column(DateTime, default=datetime.utcnow)
