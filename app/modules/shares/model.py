import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Share(Base):
    __tablename__ = "shares"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String(36), ForeignKey("files.id", ondelete="CASCADE"), nullable=False, index=True)
    share_token = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    max_access = Column(Integer, nullable=True)
    total_access = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    file = relationship("File")