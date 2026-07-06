from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import BadRequestError

BLOCKED_EXTENSIONS = {"exe", "sh", "bat", "php", "pl", "py", "js", "cgi"}

def validate_file(file: UploadFile) -> None:
    if not file.filename:
        raise BadRequestError("Nama file tidak boleh kosong.")
    
    ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ""

    if ext in BLOCKED_EXTENSIONS:
        raise BadRequestError("Format file tidak diizinkan demi keamanan.")
    
    if file.size and file.size > settings.MAX_UPLOAD_SIZE:
        max_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise BadRequestError(f"Ukuran file melebihi batas maksimal ({max_mb:.0f} MB).")