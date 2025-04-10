from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import file
# from app.api.auth import auth
from app.db.session import engine
from app.db.base import Base

from app.api.v1.endpoints import auth  # 👈 Import the auth routes

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API route registration
app.include_router(file.router, prefix="/api/v1/files", tags=["Resumes"])


# 💡 Model registration import (register models with Base)
from app.models import file as file_model  # Register ResumeFile
from app.models import user as user_model  # Register User model
 # 👈 This ensures ResumeFile is registered

# 🧱 Create tables on startup (fail safe mech.)
Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}