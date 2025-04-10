# app/db/base.py
from sqlalchemy.orm import declarative_base
# from app.models import user  # This registers the User model


Base = declarative_base()

#from app.models.file import ResumeFile