from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.config import settings
from app.limiter.token_bucket import TokenBucketLimiter
import time
from app.resolver import IdentifierResolver 


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

        response = await call_next(request)
        
        # Inject headers into successful response
        for key, value in headers.items():
            response.headers[key] = value
            
        return response