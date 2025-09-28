from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    api_name: str = "Pokemon Unite Meta Analysis API"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000

    class Config:
        env_prefix = "API_"
        env_file = ".env"


settings = APISettings()
