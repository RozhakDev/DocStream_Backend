import hashlib
import os

from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.files.model import File
from app.modules.auth.model import User

def process_file_after_upload(db: Session, file_id: str, user_id: str, storage_path: str, file_size: int):
    abs_path = os.path.join(settings.STORAGE_PATH, storage_path)

    sha256_hash = hashlib.sha256()
    try:
        with open(abs_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        checksum = sha256_hash.hexdigest()
    except FileNotFoundError:
        checksum = None

    db_file = db.query(File).filter(File.id == file_id).first()
    if db_file:
        db_file.checksum = checksum

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.storage_used = (db_user.storage_used or 0) + file_size

    db.commit()