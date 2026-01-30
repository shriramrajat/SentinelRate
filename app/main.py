# Entry point: Initializes FastAPI & mounts Middleware
from fastapi import FastAPI
from app.config import settings
from app.middleware.rate_limiter import SentinelMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# Attach our Custom Middleware
app.add_middleware(SentinelMiddleware)

@app.get("/health")
async def health_check():
    """
    Standard K8s/Docker health check.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "mode": "debug" if settings.DEBUG_MODE else "production"
    }

@app.get("/")
async def root():
    return {"message": "SentinelRate is active."}