from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.services import user_service
from app.auth.auth_handler import create_access_token

from app.auth.auth_handler import get_current_user
from fastapi import Depends

router = APIRouter()


@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(user_service.User).filter(user_service.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return user_service.create_user(db, user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": auth_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, this is a protected route"}