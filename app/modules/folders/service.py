from sqlalchemy.orm import Session

from app.modules.folders import repository, schema
from app.core.exceptions import NotFoundError, BadRequestError, ForbiddenError
from app.modules.auth.model import User

def _validate_ownership(folder, user_id: str):
    if not folder:
        raise NotFoundError(detail="Folder tidak ditemukan.")
    if folder.user_id != user_id:
        raise ForbiddenError(detail="Anda tidak memiliki akses ke folder ini.")

def _check_circular_reference(db: Session, folder_id: str, new_parent_id: str | None) -> bool:
    current_parent = new_parent_id
    while current_parent is not None:
        if current_parent == folder_id:
            return True
        parent_folder = repository.get_folder_by_id(db, current_parent)
        current_parent = parent_folder.parent_id if parent_folder else None
    return False

def create_folder(db: Session, current_user: User, folder_in: schema.FolderCreate) -> schema.FolderResponse:
    if folder_in.parent_id:
        parent_folder = repository.get_folder_by_id(db, folder_in.parent_id)
        _validate_ownership(parent_folder, current_user.id)

    if repository.check_folder_exists_in_parent(db, current_user.id, folder_in.folder_name, folder_in.parent_id):
        raise BadRequestError(detail=f"Folder dengan nama '{folder_in.folder_name}' sudah ada di lokasi ini.")
    
    return repository.create_folder(db, current_user.id, folder_in)

def list_folders(db: Session, current_user: User, parent_id: str | None = None) -> list[schema.FolderResponse]:
    if parent_id:
        parent_folder = repository.get_folder_by_id(db, parent_id)
        _validate_ownership(parent_folder, current_user.id)

    return repository.get_user_folders(db, current_user.id, parent_id)

def rename_folder(db: Session, current_user: User, folder_id: str, rename_in: schema.FolderRename) -> schema.FolderResponse:
    folder = repository.get_folder_by_id(db, folder_id)
    _validate_ownership(folder, current_user.id)

    if repository.check_folder_exists_in_parent(db, current_user.id, rename_in.folder_name, folder.parent_id):
        raise BadRequestError(detail="Nama folder sudah digunakan di lokasi ini.")
        
    folder.folder_name = rename_in.folder_name
    db.commit()
    db.refresh(folder)
    return folder

def move_folder(db: Session, current_user: User, folder_id: str, move_in: schema.FolderMove) -> schema.FolderResponse:
    folder = repository.get_folder_by_id(db, folder_id)
    _validate_ownership(folder, current_user.id)

    if move_in.parent_id:
        new_parent = repository.get_folder_by_id(db, move_in.parent_id)
        _validate_ownership(new_parent, current_user.id)

        if _check_circular_reference(db, folder_id, move_in.parent_id):
            raise BadRequestError(detail="Tidak dapat memindahkan folder ke dalam subfoldernya sendiri.")
    
    if repository.check_folder_exists_in_parent(db, current_user.id, folder.folder_name, move_in.parent_id):
        raise BadRequestError(detail="Terdapat folder dengan nama yang sama di lokasi tujuan.")

    folder.parent_id = move_in.parent_id
    db.commit()
    db.refresh(folder)
    return folder

def delete_folder(db: Session, current_user: User, folder_id: str):
    folder = repository.get_folder_by_id(db, folder_id)
    _validate_ownership(folder, current_user.id)

    if repository.get_subfolders_count(db, folder_id) > 0:
        raise BadRequestError(detail="Folder tidak kosong. Hapus atau pindahkan subfolder terlebih dahulu.")
    
    db.delete(folder)
    db.commit()