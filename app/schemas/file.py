from pydantic import BaseModel
from datetime import datetime

class ResumeFileCreate(BaseModel):
    original_filename: str
    content: str

class ResumeFileOut(BaseModel):
    id: int
    filename: str
    original_filename: str
    upload_time: datetime
    content: str

    class Config:
        orm_mode = True  # Needed to work with SQLAlchemy models
