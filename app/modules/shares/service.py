from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.shares import repository, schema
from app.modules.files.repository import get_file_by_id
from app.core.exceptions import NotFoundError, ForbiddenError, BadRequestError, UnauthorizedError
from app.core.security import verify_password
from app.modules.auth.model import User

def create_share(db: Session, current_user: User, share_in: schema.ShareCreate) -> schema.ShareResponse:
    file = get_file_by_id(db, share_in.file_id)
    if not file:
        raise NotFoundError(detail="File tidak ditemukan.")
    if file.user_id != current_user.id:
        raise ForbiddenError(detail="Anda tidak memiliki akses untuk membagikan file ini.")
    
    share = repository.create_share(db, share_in)

    response = schema.ShareResponse.model_validate(share)
    response.has_password = bool(share.password_hash)
    return response

def access_public_share(db: Session, share_token: str, access_in: schema.ShareAccess) -> schema.SharePublicResponse:
    share = repository.get_share_by_token(db, share_token)
    if not share:
        raise NotFoundError(detail="Link tidak valid atau sudah dihapus.")
    
    if share.expires_at and datetime.now(timezone.utc) > share.expires_at:
        raise ForbiddenError(detail="Link ini sudah kedaluwarsa.")
    
    if share.max_access and share.total_access >= share.max_access:
        raise ForbiddenError(detail="Link ini telah mencapai batas maksimal akses.")
    
    if share.password_hash:
        if not access_in.password:
            raise UnauthorizedError(detail="Link ini dilindungi oleh password.")
        if not verify_password(access_in.password, share.password_hash):
            raise ForbiddenError(detail="Password salah.")
        
    repository.increment_access(db, share)

    return schema.SharePublicResponse(
        share_token=share.share_token,
        file=share.file
    )

def delete_share(db: Session, current_user: User, share_id: str):
    share = repository.get_share_by_id(db, share_id)
    if not share:
        raise NotFoundError(detail="Share link tidak ditemukan.")
    
    if share.file.user_id != current_user.id:
        raise ForbiddenError(detail="Anda tidak memiliki akses.")
    
    db.delete(share)
    db.commit()