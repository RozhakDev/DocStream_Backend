from fastapi import FastAPI

from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.folders.router import router as folders_router
from app.modules.files.router import router as files_router
from app.modules.shares.router import router as shares_router
from app.modules.embeds.router import router as embeds_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    @app.get("/")
    def root():
        return {"message": "Selamat datang di API DocStream", "status": "berjalan"}
    
    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(folders_router, prefix=settings.API_V1_STR)
    app.include_router(files_router, prefix=settings.API_V1_STR)
    app.include_router(shares_router, prefix=settings.API_V1_STR)
    app.include_router(embeds_router, prefix=settings.API_V1_STR)
    
    return app

app = create_app()