from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FinHub API"

    # SQLite database file in project root
    db_url: str = "sqlite:///./finhub.db"

    class Config:
        env_file = ".env"


settings = Settings()
