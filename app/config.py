import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    UPLOAD_FOLDER = "uploads"
