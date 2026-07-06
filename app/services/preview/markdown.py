import os

from fastapi.responses import Response

from app.core.config import settings
from app.core.exceptions import NotFoundError

def render_markdown(storage_path: str) -> Response:
    abs_path = os.path.join(settings.STORAGE_PATH, storage_path)

    if not os.path.exists(abs_path):
        raise NotFoundError(detail="File fisik markdown tidak ditemukan di server.")
    
    with open(abs_path, "r", encoding="utf-8") as f:
        content = f.read()

    return Response(
        content=content,
        media_type="text/markdown",
        headers={"Content-Disposition": "inline"}
    )