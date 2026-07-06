import secrets

from sqlalchemy.orm import Session

from app.modules.shares.model import Share
from app.modules.shares.schema import ShareCreate
from app.core.security import get_password_hash

def get_share_by_id(db: Session, share_id: str) -> Share | None:
    return db.query(Share).filter(Share.id == share_id).first()

def get_share_by_token(db: Session, share_token: str) -> Share | None:
    return db.query(Share).filter(Share.share_token == share_token).first()

def get_shares_by_file(db: Session, file_id: str) -> list[Share]:
    return db.query(Share).filter(Share.file_id == file_id).all()

def create_share(db: Session, share_in: ShareCreate) -> Share:
    token = secrets.token_urlsafe(16)
    hashed_pwd = get_password_hash(share_in.password) if share_in.password else None

    db_share = Share(
        file_id=share_in.file_id,
        share_token=token,
        password_hash=hashed_pwd,
        expires_at=share_in.expires_at,
        max_access=share_in.max_access
    )
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share

def increment_access(db: Session, share: Share):
    share.total_access += 1
    db.commit()