from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://user:pass@localhost/dbname"

settings = Settings()
