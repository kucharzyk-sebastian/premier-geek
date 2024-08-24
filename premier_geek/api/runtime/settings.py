import os

from typing import TYPE_CHECKING
from typing import Any

import boto3

from pydantic import Field
from pydantic_settings import BaseSettings


if TYPE_CHECKING:
    from mypy_boto3_ssm.client import SSMClient


class Settings(BaseSettings):
    aws_region: str = Field(default=...)
    user_pool_id: str = Field(default=...)
    user_pool_client_id: str = Field(default=...)
    sport_monks_api_key_param_name: str = Field(default=...)
    sport_monks_api_key: str | None = Field(default=None)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._init_from_env_or_parameter_store()

    def _init_from_env_or_parameter_store(self) -> None:
        if self.sport_monks_api_key:
            return

        param_name = os.environ["SPORT_MONKS_API_KEY_PARAM_NAME"]
        ssm: SSMClient = boto3.client("ssm")  # type: ignore
        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
        self.sport_monks_api_key = response["Parameter"].get("Value")


settings = Settings()
