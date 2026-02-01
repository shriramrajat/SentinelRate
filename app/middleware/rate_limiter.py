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
        client_ip = request.client.host if request.client else "unknown"

        # Unpack the tuple
        is_allowed, remaining, retry_after = self.limiter.allow_request(client_ip)

        # Common Headers
        headers = {
            "X-RateLimit-Limit": str(settings.DEFAULT_LIMIT),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(int(time.time() + retry_after))
        }

        if not is_allowed:
            # Add Retry-After for blocked requests
            headers["Retry-After"] = str(int(retry_after) + 1) # +1 sec for safety
            
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "detail": f"Rate limit exceeded. Try again in {int(retry_after)+1} seconds."
                },
                headers=headers 
            )

        response = await call_next(request)
        
        # Inject headers into successful response
        for key, value in headers.items():
            response.headers[key] = value
            
        return response