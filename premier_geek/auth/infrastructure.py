from aws_cdk import Duration
from aws_cdk import RemovalPolicy
from aws_cdk.aws_cognito import AccountRecovery
from aws_cdk.aws_cognito import AuthFlow
from aws_cdk.aws_cognito import SignInAliases
from aws_cdk.aws_cognito import StandardAttribute
from aws_cdk.aws_cognito import StandardAttributes
from aws_cdk.aws_cognito import StringAttribute
from aws_cdk.aws_cognito import UserPool
from aws_cdk.aws_cognito import UserPoolClient
from constructs import Construct


class UserProfileStore(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        access_token_validity: Duration,
        id_token_validity: Duration,
        refresh_token_validity: Duration,
    ) -> None:
        super().__init__(scope, id)
        self._create_user_pool()
        self._create_user_pool_client(
            access_token_validity=access_token_validity,
            id_token_validity=id_token_validity,
            refresh_token_validity=refresh_token_validity,
        )

    def _create_user_pool(self) -> None:
        self.user_pool = UserPool(
            self,
            id="UserPool",
            account_recovery=AccountRecovery.EMAIL_AND_PHONE_WITHOUT_MFA,
            self_sign_up_enabled=True,
            sign_in_aliases=SignInAliases(email=True, phone=True, preferred_username=False, username=False),
            removal_policy=RemovalPolicy.RETAIN,
            standard_attributes=StandardAttributes(
                email=StandardAttribute(required=True, mutable=True),
                given_name=StandardAttribute(required=True, mutable=True),
                family_name=StandardAttribute(required=False, mutable=True),
                profile_picture=StandardAttribute(required=False, mutable=True),
                address=StandardAttribute(required=False, mutable=True),
            ),
            custom_attributes={"grade": StringAttribute(mutable=True), "homeGymId": StringAttribute(mutable=True)},
        )

    def _create_user_pool_client(
        self,
        *,
        access_token_validity: Duration,
        id_token_validity: Duration,
        refresh_token_validity: Duration,
    ) -> None:
        self.user_pool_client = UserPoolClient(
            self,
            id="UserPoolClient",
            user_pool=self.user_pool,
            access_token_validity=access_token_validity,
            id_token_validity=id_token_validity,
            refresh_token_validity=refresh_token_validity,
            auth_flows=AuthFlow(user_srp=True),
            generate_secret=False,
        )
        self.user_pool_client.apply_removal_policy(RemovalPolicy.RETAIN)
