from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SentinelRate"
    APP_VERSION: str = "0.1.0"
    DEBUG_MODE: bool = False
    
    # Rate Limiting Defaults (to be used later)
    DEFAULT_LIMIT: int = 100
    DEFAULT_PERIOD: int = 60  # seconds

    class Config:
        env_file = ".env"

settings = Settings()