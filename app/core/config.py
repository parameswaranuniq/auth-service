from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SIGNING_KEY: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXP: int = 900
    REFRESH_TOKEN_EXP: int = 604800


    class Config:
        env_file = ".env"


settings = Settings()