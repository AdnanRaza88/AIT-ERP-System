from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AiT ERP"
    database_url: str = "sqlite:///./ait_erp.db"
    jwt_secret: str = "change-me-in-production-ait-2025"
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 60 * 12
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()