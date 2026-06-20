from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALGORITHM: str
    SECRET_KEY: str
    REFRESH_TOKEN_EXPIRES_MINUTES: int = 15
    ACCESS_TOKEN_EXPIRES_DAYS: int = 7
    REDIS_URL: str

    class Config():
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()