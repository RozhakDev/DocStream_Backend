import logging
import time

from fastapi import Request

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DocStreamAPI")

async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - Waktu: {process_time:.4f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response