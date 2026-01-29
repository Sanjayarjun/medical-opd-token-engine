from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Medoc OPD Token Allocation Engine"
    database_url: str = "sqlite:///./medoc.db"

    class Config:
        env_file = ".env"


settings = Settings()
