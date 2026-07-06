import uuid
import os

from datetime import datetime
from fastapi import UploadFile

from app.core.config import settings
from app.utils.file import sanitize_filename, get_file_extension

async def save_upload_file(user_id: str, upload_file: UploadFile) -> tuple[str, str]:
    now = datetime.now()
    rel_dir = os.path.join(str(user_id), f"{now.year}", f"{now.month:02d}")
    abs_dir = os.path.join(settings.STORAGE_PATH, rel_dir)

    os.makedirs(abs_dir, exist_ok=True)

    safe_name = sanitize_filename(upload_file.filename)
    ext = get_file_extension(safe_name)
    disk_filename = f"{uuid.uuid4().hex}.{ext}"

    rel_path = os.path.join(rel_dir, disk_filename)
    abs_path = os.path.join(abs_dir, disk_filename)

    try:
        with open(abs_path, "wb") as buffer:
            while chunk := await upload_file.read(1024 * 1024):  # Baca per 1 MB
                buffer.write(chunk)
    finally:
        await upload_file.seek(0)

    return rel_path, safe_name

def delete_file_from_disk(rel_path: str):
    abs_path = os.path.join(settings.STORAGE_PATH, rel_path)
    if os.path.exists(abs_path):
        os.remove(abs_path)