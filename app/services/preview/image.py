import os

from fastapi.responses import FileResponse

from app.core.config import settings

def render_image(storage_path: str, mime_type: str) -> FileResponse:
    abs_path = os.path.join(settings.STORAGE_PATH, storage_path)

    return FileResponse(
        path=abs_path,
        media_type=mime_type,
        headers={
            "Cache-Control": "public, max-age=86400, immutable",
            "Content-Disposition": "inline"
        }
    )