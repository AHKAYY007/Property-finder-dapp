from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Property Finder"
    API_V1_STR: str = "/api/v1"
    
    # Backend URL
    BACKEND_URL: str = "http://localhost:8000"
    
    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"
    
    # PostgreSQL
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str | None = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: str | None, values: dict) -> str:
        if v:
            return v
        return f"postgresql://{values['POSTGRES_USER']}:{values['POSTGRES_PASSWORD']}@{values['POSTGRES_SERVER']}/{values['POSTGRES_DB']}"

    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # Next.js frontend
    ]

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # IPFS
    IPFS_URL: str = "http://localhost:5001"
    IPFS_GATEWAY: str = "http://localhost:8080"

    # Sui
    SUI_RPC_URL: str = "https://fullnode.testnet.sui.io:443"
    SUI_NETWORK: str = "testnet"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 