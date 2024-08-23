from pathlib import Path

from aws_cdk import Duration
from aws_cdk.aws_lambda import Architecture
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_lambda import FunctionUrlAuthType
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_logs import LogGroup
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct
from poetry_asset_code import PoetryAssetCode


class Api(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        user_pool_id: str,
        user_pool_client_id: str,
    ) -> None:
        super().__init__(scope, id)
        self.create_api_function(
            user_pool_id=user_pool_id,
            user_pool_client_id=user_pool_client_id,
        )

    def create_api_function(
        self,
        *,
        user_pool_id: str,
        user_pool_client_id: str,
    ) -> None:
        self.function = Function(
            self,
            "Function",
            code=PoetryAssetCode(str(Path(__file__).parent.resolve()), deploy_time=True),
            handler="runtime.main.handler",
            runtime=Runtime.PYTHON_3_12,
            architecture=Architecture.X86_64,
            memory_size=128,
            timeout=Duration.seconds(25),
            log_group=LogGroup(
                self,
                "LogGroup",
                retention=RetentionDays.ONE_WEEK,
            ),
            environment={
                "COGNITO__USER_POOL_ID": user_pool_id,
                "COGNITO__USER_POOL_CLIENT_ID": user_pool_client_id,
            },
        )

        self.function_url = self.function.add_function_url(auth_type=FunctionUrlAuthType.NONE)
