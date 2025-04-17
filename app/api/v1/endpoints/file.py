from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.file import ResumeFileOut, ResumeFileCreate
from app.services.file_service import save_resume_file, search_resumes
from app.db.session import SessionLocal
from app.auth.auth_handler import get_current_user  # 👈 Auth dependency
from app.models.user import User  # 👈 Authenticated user type
from app.models.file import ResumeFile as FileModel 
from app.db.session import get_db  # Make sure this is already imported
import traceback  # 👈 NEW: for detailed error logging
import PyPDF2 # 👈 NEW: for PDF file handling
from sqlalchemy import or_
import uuid 
import os  # For file system operations
from app.core.config import settings
from app.utils.utils import extract_text_from_pdf

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=ResumeFileOut)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        print(f"File received: {file.filename}, content_type: {file.content_type}")  # 👀 Debug

        if not file.filename.lower().endswith(".pdf") :
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
         # Extract content from the PDF file
        unique_name = f"{uuid.uuid4().hex}_{file.filename}"
        save_path = os.path.join(settings.FILE_UPLOAD_DIR, unique_name)
        os.makedirs(settings.FILE_UPLOAD_DIR, exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(file.file.read())

        content = extract_text_from_pdf(save_path)  # Extract content from the PDF

        # try:
        #     pdf_reader = PyPDF2.PdfReader(file.file)
        #     for page in pdf_reader.pages:
        #         content += page.extract_text()
        # except Exception as e:
        #     raise HTTPException(status_code=400, detail="Failed to extract content from the PDF file")
        file_data = ResumeFileCreate(original_filename=file.filename,content=content)
        result = save_resume_file(db, file_data, file)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/search", response_model=list[ResumeFileOut])
def search_resume(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
           # Query the database for files matching the query in name or content
        results = db.query(FileModel).filter(
            or_(
                FileModel.original_filename.like(f"%{q}%"),  # Search in file name
                FileModel.content.like(f"%{q}%")  # Search in file content
            )
        ).all()
        return results
    except Exception as e:
        traceback.print_exc()  # 👈 Print error in terminal
        raise HTTPException(status_code=500, detail=str(e))
