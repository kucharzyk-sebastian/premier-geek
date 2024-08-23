from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_region: str = Field(default=...)
    user_pool_id: str = Field(default=...)
    user_pool_client_id: str = Field(default=...)


settings = Settings()
