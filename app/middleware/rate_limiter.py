from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.config import settings
from app.limiter.token_bucket import TokenBucketLimiter

class SentinelMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Initialize the Engine
        # Refill Rate = Limit / Period (e.g., 100 tokens / 60 seconds)
        refill_rate = settings.DEFAULT_LIMIT / settings.DEFAULT_PERIOD
        
        self.limiter = TokenBucketLimiter(
            capacity=settings.DEFAULT_LIMIT,
            refill_rate=refill_rate
        )

    async def dispatch(self, request: Request, call_next):
        # 1. Identity: Extract IP (The "Who")
        # In PROD, you would use X-Forwarded-For headers behind a proxy
        client_ip = request.client.host if request.client else "unknown"

        # 2. Decision: Ask the Engine
        is_allowed = self.limiter.allow_request(client_ip)

        # 3. Enforce: Block if false
        if not is_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "detail": "Rate limit exceeded. Slow down."
                }
            )

        # 4. Allow: Forward the request
        response = await call_next(request)
        
        # Add headers for transparency
        response.headers["X-RateLimit-Limit"] = str(settings.DEFAULT_LIMIT)
        return response