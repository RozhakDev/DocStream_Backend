from sqlalchemy.orm import Session

from app.modules.files.model import File

def get_file_by_id(db: Session, file_id: str) -> File | None:
    return db.query(File).filter(File.id == file_id).first()

def get_user_files(db: Session, user_id: str, folder_id: str | None = None) -> list[File]:
    return db.query(File).filter(
        File.user_id == user_id,
        File.folder_id == folder_id
    ).all()

def check_filename_exists(db: Session, user_id: str, folder_id: str | None, filename: str) -> bool:
    return db.query(File).filter(
        File.user_id == user_id,
        File.folder_id == folder_id,
        File.filename == filename
    ).first() is not None