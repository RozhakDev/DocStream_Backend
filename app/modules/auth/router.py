from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.auth import schema, service, model

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: schema.UserCreate, db: Session = Depends(get_db)):
    return service.register_user(db, user_in)

@router.post("/login", response_model=schema.TokenResponse)
def login(credentials: schema.UserLogin, db: Session = Depends(get_db)):
    return service.authenticate_user(db, credentials)

@router.get("/me", response_model=schema.UserResponse)
def get_me(current_user: model.User = Depends(get_current_user)):
    return current_user