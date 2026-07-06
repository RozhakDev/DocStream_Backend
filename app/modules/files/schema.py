from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FileResponse(BaseModel):
    id: str
    user_id: str
    folder_id: Optional[str] = None
    filename: str
    original_filename: str
    file_extension: str
    mime_type: str
    file_size: int
    visibility: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FileRename(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)

class FileMove(BaseModel):
    folder_id: Optional[str] = Field(None, description="Pindah ke root (null) atau folder_id tertentu")