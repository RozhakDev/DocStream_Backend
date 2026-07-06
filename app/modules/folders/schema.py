from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FolderCreate(BaseModel):
    folder_name: str = Field(..., min_length=1, max_length=255, example="Dokumen Penting")
    parent_id: Optional[str] = Field(None, description="ID dari folder induk. Kosongkan jika root.")

class FolderRename(BaseModel):
    folder_name: str = Field(..., min_length=1, max_length=255)

class FolderMove(BaseModel):
    parent_id: Optional[str] = Field(None, description="Pindahkan ke root (null) atau ke folder lain")

class FolderResponse(BaseModel):
    id: str
    user_id: str
    parent_id: Optional[str] = None
    folder_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True