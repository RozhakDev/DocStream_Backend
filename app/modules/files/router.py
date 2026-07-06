from fastapi import APIRouter, Depends, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.auth.model import User
from app.modules.files import schema, service, repository

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload", response_model=schema.FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    folder_id: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await service.upload_file(db, current_user, file, background_tasks, folder_id)

@router.get("/", response_model=List[schema.FileResponse])
def get_files(
    folder_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return repository.get_user_files(db, current_user.id, folder_id)

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service.delete_file(db, current_user, file_id)