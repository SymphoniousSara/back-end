from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator, Field


class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    DATABASE_URL: str = ''
    PROJECT_NAME: str = "Symphony Birthday Planner"
    ALLOWED_ORIGINS: str = ""

    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field(..., env="POSTGRES_PORT")

    PGADMIN_EMAIL: str = Field(..., env="PGADMIN_EMAIL")
    PGADMIN_PASSWORD: str = Field(..., env="PGADMIN_PASSWORD")

    DATABASE_URL: str = ""

    # Company Email Domain
    COMPANY_EMAIL_DOMAIN: str = "symphony.is"

    GOOGLE_CLIENT_ID: str = Field(..., env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(..., env="GOOGLE_CLIENT_SECRET")
    REDIRECT_URI: str = Field(..., env="REDIRECT_URI")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")

    # Splitting the 2 values in the .env file and returning a string list
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(',') if v else []

    # This is a configuration for loading the env variables correctly
    class Config:
        env_file = ".env"
        extra = "allow"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
