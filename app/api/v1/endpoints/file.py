from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.file import ResumeFileOut, ResumeFileCreate
from app.services.file_service import save_resume_file, search_resumes
from app.db.session import SessionLocal
from app.auth.auth_handler import get_current_user  # 👈 Auth dependency
from app.models.user import User  # 👈 Authenticated user type
from app.db.session import get_db  # Make sure this is already imported
import traceback  # 👈 NEW: for detailed error logging

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

        file_data = ResumeFileCreate(original_filename=file.filename)
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
        results = search_resumes(db, q)
        return results
    except Exception as e:
        traceback.print_exc()  # 👈 Print error in terminal
        raise HTTPException(status_code=500, detail=str(e))
