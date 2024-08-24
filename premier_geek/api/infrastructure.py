from pathlib import Path

from aws_cdk import Aws
from aws_cdk import Duration
from aws_cdk.aws_iam import Effect
from aws_cdk.aws_iam import PolicyStatement
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
        sport_monks_api_key_param_name: str,
    ) -> None:
        super().__init__(scope, id)
        self._create_api_function(
            user_pool_id=user_pool_id,
            user_pool_client_id=user_pool_client_id,
            sport_monks_api_key_param_name=sport_monks_api_key_param_name,
        )

    def _create_api_function(
        self,
        *,
        user_pool_id: str,
        user_pool_client_id: str,
        sport_monks_api_key_param_name: str,
    ) -> None:
        model_arn = f"arn:{Aws.PARTITION}:bedrock:{Aws.REGION}::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"

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
                "USER_POOL_ID": user_pool_id,
                "USER_POOL_CLIENT_ID": user_pool_client_id,
                "SPORT_MONKS_API_KEY_PARAM_NAME": sport_monks_api_key_param_name,
                "MODEL_ARN": model_arn,
            },
            initial_policy=[
                PolicyStatement(
                    actions=[
                        "ssm:GetParameter",
                    ],
                    effect=Effect.ALLOW,
                    resources=[
                        f"arn:{Aws.PARTITION}:ssm:{Aws.REGION}:{Aws.ACCOUNT_ID}:parameter{sport_monks_api_key_param_name}"
                    ],
                ),
                PolicyStatement(
                    actions=[
                        "bedrock:InvokeModel",
                    ],
                    effect=Effect.ALLOW,
                    resources=[model_arn],
                ),
            ],
        )

        self.function_url = self.function.add_function_url(auth_type=FunctionUrlAuthType.NONE)
