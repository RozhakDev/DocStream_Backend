import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, BigInteger, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    folder_id = Column(String(36), ForeignKey("folders.id", ondelete="SET NULL"), nullable=True, index=True)

    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_extension = Column(String(50), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    storage_path = Column(String(500), nullable=False)
    visibility = Column(String(20), default="private", nullable=False) # 'private' atau 'public'
    checksum = Column(String(64), nullable=True)

    total_views = Column(Integer, default=0)
    total_downloads = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User")
    folder = relationship("Folder")