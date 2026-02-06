from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.config import settings
from app.limiter.token_bucket import TokenBucketLimiter
import time
from app.resolver import IdentifierResolver 
from app.metrics import MetricsManager

class SentinelMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Initialize Engine (Empty now)
        self.limiter = TokenBucketLimiter() 
    async def dispatch(self, request: Request, call_next):
        # 1. Resolve Identity
        identifier, is_auth = IdentifierResolver.resolve_identity(request)
        # 2. Select Policy
        if is_auth:
            limit = settings.USER_LIMIT
        else:
            limit = settings.ANON_LIMIT
            
        rate = limit / settings.DEFAULT_PERIOD
        # 3. Decision
        is_allowed, remaining, retry_after = self.limiter.allow_request(
            identifier=identifier,
            capacity=limit,
            refill_rate=rate
        )

        # Common Headers for decision
        headers = {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(int(time.time() + retry_after))
        }

        if not is_allowed:
            # 🚨 TRACK BLOCK
            MetricsManager.track_blocked()

            # Add Retry-After for blocked requests
            headers["Retry-After"] = str(int(retry_after) + 1)
            
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "detail": f"Rate limit exceeded. Try again in {int(retry_after)+1} seconds."
                },
                headers=headers 
            )

        # ✅ TRACK ALLOW
        MetricsManager.track_allowed()

        response = await call_next(request)
        
        # Inject headers into successful response
        for key, value in headers.items():
            response.headers[key] = value
            
        return response