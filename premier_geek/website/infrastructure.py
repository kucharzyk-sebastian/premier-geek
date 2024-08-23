import pathlib

from typing import Any

from aws_cdk import RemovalPolicy
from aws_cdk.aws_cloudfront import Distribution
from aws_cdk.aws_cloudfront import ViewerProtocolPolicy
from aws_cdk.aws_cloudfront_origins import S3Origin
from aws_cdk.aws_s3 import BlockPublicAccess
from aws_cdk.aws_s3 import Bucket
from constructs import Construct
from react_bucket_deployment import ReactBucketDeployment


class Website(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs: Any) -> None:
        super().__init__(scope, id, **kwargs)
        self._create_bucket()
        self._create_distribution()
        self._create_deployment()

    def _create_bucket(self) -> None:
        self.bucket = Bucket(
            self,
            "Bucket",
            website_index_document="index.html",
            website_error_document="index.html",
            block_public_access=BlockPublicAccess.BLOCK_ACLS,
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

    def _create_distribution(self) -> None:
        self.distribution = Distribution(
            self,
            "Distribution",
            default_behavior={
                "origin": S3Origin(self.bucket),
                "viewer_protocol_policy": ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            },
        )

    def _create_deployment(self) -> None:
        self.deployment = ReactBucketDeployment(
            self,
            "Deployment",
            sources=str(pathlib.Path(__file__).parent.resolve() / "runtime"),
            destination_bucket=self.bucket,
            distribution=self.distribution,
        )
