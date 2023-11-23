import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_PERMANENT = False
    UPLOAD_FOLDER = "uploads"
