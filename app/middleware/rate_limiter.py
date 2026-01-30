from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class SentinelMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Placeholder: This is where we will inspect every request
        # 1. Extract Identity
        # 2. Check Limits
        # 3. Allow or Block
        
        response = await call_next(request)
        
        # Placeholder header to prove it's alive
        response.headers["X-Sentinel-Status"] = "Monitoring"
        return response