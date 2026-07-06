import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.core.database import Base

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String(36), ForeignKey("files.id", ondelete="CASCADE"), index=True, nullable=False)
    event_type = Column(String(50), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    accessed_at = Column(DateTime(timezone=True), server_default=func.now())