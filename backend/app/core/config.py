from pathlib import Path
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project Root
BASE_DIR = Path(__file__).resolve().parents[3]

# Load .env
load_dotenv(BASE_DIR / ".env")

GOOGLE_SAFE_BROWSING_API_KEY = os.getenv(
    "GOOGLE_SAFE_BROWSING_API_KEY"
)

VIRUSTOTAL_API_KEY = os.getenv(
    "VIRUSTOTAL_API_KEY"
)

ABUSEIPDB_API_KEY = os.getenv(
    "ABUSEIPDB_API_KEY"
)

PHISHTANK_API_KEY = os.getenv(
    "PHISHTANK_API_KEY"
)
ALIENVAULT_OTX_API_KEY = os.getenv(
    "ALIENVAULT_OTX_API_KEY"
)

class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "escudoflow"

    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    cors_origins: str = "http://localhost:8080,http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
