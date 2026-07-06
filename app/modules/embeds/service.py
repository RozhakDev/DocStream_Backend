import os

from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.exceptions import NotFoundError, ForbiddenError, UnauthorizedError
from app.core.config import settings
from app.utils.token import decode_token
from app.modules.files.repository import get_file_by_id
from app.modules.shares.repository import get_share_by_token
from app.modules.auth.repository import get_user_by_id
from app.modules.files.model import File

def get_authorized_file_for_embed(
    db: Session,
    file_id: str,
    auth_token: str | None,
    share_token: str | None
) -> File:
    file = get_file_by_id(db, file_id)
    if not file:
        raise NotFoundError(detail="File tidak ditemukan.")
    
    if share_token:
        share = get_share_by_token(db, share_token)
        if not share or share.file_id != file_id:
            raise NotFoundError(detail="Share token tidak valid.")
        
        if share.expires_at and datetime.now(timezone.utc) > share.expires_at:
            raise ForbiddenError(detail="Link berbagi sudah kedaluwarsa.")
        
        if share.password_hash:
            raise ForbiddenError(detail="File dilindungi sandi. Tidak dapat di-embed secara langsung.")
        
        return file

    if auth_token:
        try:
            payload = decode_token(auth_token)
            user_id = payload.get("sub")
            if file.user_id == user_id:
                return file
        except Exception:
            raise UnauthorizedError(detail="Token otentikasi tidak valid atau sudah kedaluwarsa.")
        
        raise ForbiddenError(detail="Anda tidak memiliki izin untuk melihat file ini.")
    
def get_absolute_file_path(storage_path: str) -> str:
    path = os.path.join(settings.STORAGE_PATH, storage_path)
    if not os.path.exists(path):
        raise NotFoundError(detail="File fisik tidak ditemukan di server.")
    return path