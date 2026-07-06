import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import DocStreamException

from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.folders.router import router as folders_router
from app.modules.files.router import router as files_router
from app.modules.shares.router import router as shares_router
from app.modules.embeds.router import router as embeds_router

from app.middleware.logging import log_requests_middleware
from app.middleware.ratelimit import rate_limit_middleware

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(log_requests_middleware)
    app.middleware("http")(rate_limit_middleware)

    @app.exception_handler(DocStreamException)
    async def docstream_exception_handler(request: Request, exc: DocStreamException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None)
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Terjadi kesalahan pada server. Silakan hubungi administrator."}
        )

    @app.get("/", tags=["Health Check"])
    def health_check():
        return {
            "app": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "berjalan normal"
        }
    
    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(folders_router, prefix=settings.API_V1_STR)
    app.include_router(files_router, prefix=settings.API_V1_STR)
    app.include_router(shares_router, prefix=settings.API_V1_STR)
    app.include_router(embeds_router, prefix=settings.API_V1_STR)
    
    return app

app = create_app()