from sqlalchemy.orm import Session

from app.modules.auth.model import User
from app.modules.auth.schema import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user