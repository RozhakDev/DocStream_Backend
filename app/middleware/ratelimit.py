import time

from fastapi import Request, status
from fastapi.responses import JSONResponse
from collections import defaultdict

RATE_LIMIT = 100
PER_SECONDS = 60

_ip_records = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
         return await call_next(request)
    
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()

    _ip_records[client_ip] = [t for t in _ip_records[client_ip] if current_time - t < PER_SECONDS]

    if len(_ip_records[client_ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Terlalu banyak permintaan. Silakan coba lagi sebentar lagi."}
        )
    
    _ip_records[client_ip].append(current_time)
    
    return await call_next(request)