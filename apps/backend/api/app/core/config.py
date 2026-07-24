from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    app_name: str = "Interservim AI Sales Agent"
    debug: bool = True
    api_prefix: str = "/api/v1"

    database_url: str = "postgresql://interservim:interservim_pass@localhost:5432/interservim_ai"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change-this-to-a-random-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 7

    ai_provider: str = "openai"
    ai_api_key: str = ""
    ai_model: str = "gpt-4o"
    ai_temperature: float = 0.7
    ai_max_tokens: int = 1024

    whatsapp_provider: str = "meta"
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_verify_token: str = ""
    whatsapp_api_version: str = "v21.0"

    cors_origins: str = "http://localhost:3000,http://localhost:8080"
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 50

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
