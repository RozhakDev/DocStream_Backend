from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.auth.model import User
from app.modules.shares import schema, service

router = APIRouter(prefix="/shares", tags=["Shares"])

@router.post("/create", response_model=schema.ShareResponse, status_code=status.HTTP_201_CREATED)
def create_share(
    share_in: schema.ShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.create_share(db, current_user, share_in)

@router.post("/{share_token}/access", response_model=schema.SharePublicResponse)
def access_share(
    share_token: str,
    access_in: schema.ShareAccess,
    db: Session = Depends(get_db)
):
    return service.access_public_share(db, share_token, access_in)