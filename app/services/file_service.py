import os
from sqlalchemy.orm import Session
from app.models.file import ResumeFile
from app.schemas.file import ResumeFileCreate
from app.core.config import settings
from datetime import datetime
import uuid

def save_resume_file(db: Session, file_data: ResumeFileCreate, uploaded_file) -> ResumeFile:
    # Generate a unique filename
    unique_name = f"{uuid.uuid4().hex}_{file_data.original_filename}"
    save_path = os.path.join(settings.FILE_UPLOAD_DIR, unique_name)

    # Ensure directory exists
    os.makedirs(settings.FILE_UPLOAD_DIR, exist_ok=True)

    # Save the file to disk
    with open(save_path, "wb") as f:
        f.write(uploaded_file.file.read())

    # Save metadata to DB
    db_file = ResumeFile(
        filename=unique_name,
        original_filename=file_data.original_filename,
        upload_time=datetime.utcnow()
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def search_resumes(db: Session, query: str):
    return db.query(ResumeFile).filter(
        ResumeFile.original_filename.ilike(f"%{query}%")
    ).all()
