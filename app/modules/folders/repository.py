from sqlalchemy.orm import Session

from app.modules.folders.model import Folder
from app.modules.folders.schema import FolderCreate

def get_folder_by_id(db: Session, folder_id: str) -> Folder | None:
    return db.query(Folder).filter(Folder.id == folder_id).first()

def get_user_folders(db: Session, user_id: str, parent_id: str | None = None) -> list[Folder]:
    return db.query(Folder).filter(
        Folder.user_id == user_id,
        Folder.parent_id == parent_id
    ).all()

def check_folder_exists_in_parent(db: Session, user_id: str, folder_name: str, parent_id: str | None) -> bool:
    return db.query(Folder).filter(
        Folder.user_id == user_id,
        Folder.parent_id == parent_id,
        Folder.folder_name == folder_name
    ).first() is not None

def create_folder(db: Session, user_id: str, folder_in: FolderCreate) -> Folder:
    db_folder = Folder(
        user_id=user_id,
        folder_name=folder_in.folder_name,
        parent_id=folder_in.parent_id
    )
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder

def get_subfolders_count(db: Session, folder_id: str) -> int:
    return db.query(Folder).filter(Folder.parent_id == folder_id).count()