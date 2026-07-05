from fastapi import FastAPI

from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    @app.get("/")
    def root():
        return {"message": "Selamat datang di API DocStream", "status": "berjalan"}
    
    return app

app = create_app()