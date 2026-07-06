from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.modules.files.schema import FileResponse

class ShareCreate(BaseModel):
    file_id: str = Field(..., description="ID dari file yang akan dibagikan")
    password: Optional[str] = Field(None, min_length=4, description="Password untuk proteksi link (opsional)")
    expires_at: Optional[datetime] = Field(None, description="Waktu kedaluwarsa link (opsional)")
    max_access: Optional[int] = Field(None, ge=1, description="Batas maksimal akses link (opsional)")

class ShareResponse(BaseModel):
    id: str
    file_id: str
    share_token: str
    has_password: bool
    expires_at: Optional[datetime]
    max_access: Optional[int]
    total_access: int
    created_at: datetime

    class Config:
        from_attributes = True

class ShareAccess(BaseModel):
    password: Optional[str] = None
    
class SharePublicResponse(BaseModel):
    share_token: str
    file: FileResponse