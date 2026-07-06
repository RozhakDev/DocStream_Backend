import os

from fastapi.responses import FileResponse

from app.core.config import settings

def render_pdf(storage_path: str) -> FileResponse:
    abs_path = os.path.join(settings.STORAGE_PATH, storage_path)

    return FileResponse(
        path=abs_path,
        media_type="application/pdf",
        headers={
            "Cache-Control": "no-cache",
            "Content-Disposition": "inline"
        }
    )