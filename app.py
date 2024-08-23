import os

import aws_cdk as cdk

from premier_geek.component import PremierGeek


app = cdk.App()
PremierGeek(
    app,
    "pocPremierGeek",
    env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")),
    access_token_validity=cdk.Duration.days(1),
    id_token_validity=cdk.Duration.days(1),
    refresh_token_validity=cdk.Duration.days(2),
)

app.synth()
