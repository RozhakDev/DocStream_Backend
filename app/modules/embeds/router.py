from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.embeds import service
from app.services.preview import image, pdf, markdown

router = APIRouter(prefix="/embed", tags=["Embeds & Preview"])

@router.get("/raw/{file_id}")
def get_raw_file(
    file_id: str,
    token: str = Query(None, description="Akses token pengguna untuk file privat"),
    share_token: str = Query(None, description="Share token untuk file publik"),
    db: Session = Depends(get_db)
):
    file = service.get_authorized_file_for_embed(db, file_id, auth_token=token, share_token=share_token)
    abs_path = service.get_absolute_file_path(file.storage_path)

    return FileResponse(
        path=abs_path,
        media_type=file.mime_type,
        filename=file.original_filename
    )

@router.get("/image/{file_id}")
def embed_image(
    file_id: str,
    token: str = Query(None),
    share_token: str = Query(None),
    db: Session = Depends(get_db)
):
    file = service.get_authorized_file_for_embed(db, file_id, auth_token=token, share_token=share_token)

    if not file.mime_type.startswith("image/"):
        return {"error": "Format file bukan gambar"}
    
    return image.render_image(file.storage_path, file.mime_type)

@router.get("/iframe/{file_id}")
def embed_iframe(
    file_id: str,
    token: str = Query(None),
    share_token: str = Query(None),
    db: Session = Depends(get_db)
):
    file = service.get_authorized_file_for_embed(db, file_id, auth_token=token, share_token=share_token)

    if file.mime_type == "application/pdf":
        return pdf.render_pdf(file.storage_path)
    elif file.file_extension.lower() in ["md", "markdown"]:
        return markdown.render_markdown(file.storage_path)
    
    abs_path = service.get_absolute_file_path(file.storage_path)
    return FileResponse(path=abs_path, media_type=file.mime_type, headers={"Content-Disposition": "inline"})