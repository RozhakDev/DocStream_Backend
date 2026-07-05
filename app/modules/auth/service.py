from sqlalchemy.orm import Session

from app.modules.auth import repository, schema
from app.core.exceptions import BadRequestError, UnauthorizedError
from app.core.security import verify_password
from app.utils.token import create_access_token, create_refresh_token

def register_user(db: Session, user_in: schema.UserCreate) -> schema.UserResponse:
    user = repository.get_user_by_email(db, user_in.email)
    if user:
        raise BadRequestError(detail="Email sudah terdaftar.")
    
    new_user = repository.create_user(db, user_in)
    return new_user

def authenticate_user(db: Session, credentials: schema.UserLogin) -> schema.TokenResponse:
    user = repository.get_user_by_email(db, credentials.email)

    if not user or not verify_password(credentials.password, user.password_hash):
        raise UnauthorizedError(detail="Email atau password salah.")
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return schema.TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )