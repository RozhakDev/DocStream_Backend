from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.auth import schema, service, model

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: schema.UserCreate, db: Session = Depends(get_db)):
    return service.register_user(db, user_in)

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=schema.TokenResponse)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_login = schema.UserLogin(email=credentials.username, password=credentials.password)
    return service.authenticate_user(db, user_login)

@router.get("/me", response_model=schema.UserResponse)
def get_me(current_user: model.User = Depends(get_current_user)):
    return current_user