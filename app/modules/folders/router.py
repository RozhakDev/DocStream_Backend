from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.auth.model import User
from app.modules.folders import schema, service

router = APIRouter(prefix="/folders", tags=["Folders"])

@router.post("/", response_model=schema.FolderResponse, status_code=status.HTTP_201_CREATED)
def create_folder(
    folder_in: schema.FolderCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.create_folder(db, current_user, folder_in)

@router.get("/", response_model=List[schema.FolderResponse])
def get_folders(
    parent_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.list_folders(db, current_user, parent_id)

@router.patch("/{folder_id}/rename", response_model=schema.FolderResponse)
def rename_folder(
    folder_id: str,
    rename_in: schema.FolderRename,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.rename_folder(db, current_user, folder_id, rename_in)

@router.patch("/{folder_id}/move", response_model=schema.FolderResponse)
def move_folder(
    folder_id: str,
    move_in: schema.FolderMove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.move_folder(db, current_user, folder_id, move_in)

@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_folder(
    folder_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service.delete_folder(db, current_user, folder_id)