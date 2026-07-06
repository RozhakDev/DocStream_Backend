from sqlalchemy.orm import Session
from fastapi import UploadFile, BackgroundTasks

from app.modules.files import repository, schema, validator
from app.modules.files.model import File
from app.modules.folders.repository import get_folder_by_id
from app.core.exceptions import NotFoundError, ForbiddenError, BadRequestError
from app.modules.auth.model import User
from app.services.storage import local as storage_service
from app.utils.file import get_file_extension
from app.services.background.tasks import process_file_after_upload

def _validate_ownership(file: File, user_id: str):
    if not file:
        raise NotFoundError(detail="File tidak ditemukan.")
    if file.user_id != user_id:
        raise ForbiddenError(detail="Anda tidak memiliki akses ke file ini.")
    
async def upload_file(
    db: Session, current_user: User, upload_file: UploadFile, 
    background_tasks: BackgroundTasks, folder_id: str | None = None
) -> schema.FileResponse:
    validator.validate_file(upload_file)

    if folder_id:
        folder = get_folder_by_id(db, folder_id)
        if not folder or folder.user_id != current_user.id:
            raise ForbiddenError(detail="Folder tujuan tidak valid atau Anda tidak memiliki akses.")

    rel_path, safe_name = await storage_service.save_upload_file(current_user.id, upload_file)

    final_name = safe_name
    counter = 1
    ext = get_file_extension(safe_name)
    base_name = safe_name.rsplit('.', 1)[0] if '.' in safe_name else safe_name

    while repository.check_filename_exists(db, current_user.id, folder_id, final_name):
        final_name = f"{base_name}({counter}).{ext}"
        counter += 1

    file_size = upload_file.size or 0

    db_file = File(
        user_id=current_user.id,
        folder_id=folder_id,
        filename=final_name,
        original_filename=upload_file.filename,
        file_extension=ext,
        mime_type=upload_file.content_type or "application/octet-stream",
        file_size=file_size,
        storage_path=rel_path
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    background_tasks.add_task(
        process_file_after_upload,
        db=db, file_id=db_file.id, user_id=current_user.id, 
        storage_path=rel_path, file_size=file_size
    )

    return db_file

def delete_file(db: Session, current_user: User, file_id: str):
    file = repository.get_file_by_id(db, file_id)
    _validate_ownership(file, current_user.id)

    storage_service.delete_file_from_disk(file.storage_path)

    current_user.storage_used = max(0, (current_user.storage_used or 0) - file.file_size)

    db.delete(file)
    db.commit()