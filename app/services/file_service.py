import os
from sqlalchemy.orm import Session
from app.models.file import ResumeFile
from app.schemas.file import ResumeFileCreate
from app.core.config import settings
from datetime import datetime
import uuid
from PyPDF2 import PdfReader

def save_resume_file(db: Session, file_data: ResumeFileCreate, uploaded_file) -> ResumeFile:
    # Generate a unique filename
    unique_name = f"{uuid.uuid4().hex}_{file_data.original_filename}"
    save_path = os.path.join(settings.FILE_UPLOAD_DIR, unique_name)

    # Ensure directory exists
    os.makedirs(settings.FILE_UPLOAD_DIR, exist_ok=True)

    # Save the file to disk
    with open(save_path, "wb") as f:
        f.write(uploaded_file.file.read())

    text_content = extract_text_from_pdf(save_path)


    # Save metadata to DB
    db_file = ResumeFile(
        filename=unique_name,
        original_filename=file_data.original_filename,
        upload_time=datetime.utcnow(),
        content=file_data.content
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def search_resumes(db: Session, query: str):
    return db.query(ResumeFile).filter(
        (ResumeFile.original_filename.ilike(f"%{query}%")) |
        (ResumeFile.content.ilike(f"%{query}%"))
    ).all()


def extract_text_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
