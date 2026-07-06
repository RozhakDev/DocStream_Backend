from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.modules.analytics.model import Analytics
from app.modules.files.model import File

def record_analytics_task(file_id: str, event_type: str, ip_address: str, user_agent: str):
    db: Session = SessionLocal()
    try:
        log_entry = Analytics(
            file_id=file_id,
            event_type=event_type,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(log_entry)

        file_record = db.query(File).filter(File.id == file_id).first()
        if file_record:
            if event_type == "view":
                file_record.total_views = (file_record.total_views or 0) + 1
            elif event_type == "download":
                file_record.total_downloads = (file_record.total_downloads or 0) + 1

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[Analytics Error] Gagal mencatat event: {e}")
    finally:
        db.close()