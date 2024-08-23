from typing import Any

from aws_cdk import Duration
from aws_cdk import Stack
from constructs import Construct

from premier_geek.api.infrastructure import Api
from premier_geek.auth.infrastructure import UserProfileStore


class PremierGeek(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        access_token_validity: Duration,
        id_token_validity: Duration,
        refresh_token_validity: Duration,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.user_profile_store = UserProfileStore(
            self,
            "UserProfileStore",
            access_token_validity=access_token_validity,
            id_token_validity=id_token_validity,
            refresh_token_validity=refresh_token_validity,
        )
        self.api = Api(
            self,
            "Api",
            user_pool_id=self.user_profile_store.user_pool.user_pool_id,
            user_pool_client_id=self.user_profile_store.user_pool_client.user_pool_client_id,
        )
