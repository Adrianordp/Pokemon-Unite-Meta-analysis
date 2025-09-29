from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    api_name: str = "Pokemon Unite Meta Analysis API"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000

    model_config = ConfigDict(env_file=".env", env_prefix="API_")


settings = APISettings()
