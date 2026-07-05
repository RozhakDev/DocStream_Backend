from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.core.exceptions import UnauthorizedError
from app.utils.token import decode_token
from app.modules.auth.repository import get_user_by_id
from app.modules.auth.model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise UnauthorizedError(detail="Kredensial tidak valid.")
    except JWTError:
        raise UnauthorizedError(detail="Pengguna tidak ditemukan.")
    
    user = get_user_by_id(db, user_id=user_id)
    if user is None:
        raise UnauthorizedError(detail="Pengguna tidak ditemukan.")

    return user