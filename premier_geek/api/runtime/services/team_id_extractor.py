import json

from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
from mypy_boto3_bedrock_runtime.type_defs import InvokeModelResponseTypeDef
from runtime.repositories.teams_repository import Team


class TeamIdExtractor:
    _MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
    _MAX_TOKENS_TO_SAMPLE = 10
    _SYSTEM_PROMPT_TEMPLATE = """
Your job is to identify the team's name from the English Premier League that the user refers to in their query.  If you can't assign a team to the user's query, reply with "None". For example:

Q: What is Manchester United's squad?
A: 14
Q: Show me The Hammers squad.
A: 1
Q: Who plays for Chelsea?
A: 18
Q: Do you like football?
A: None

Here is a JSON list of teams with corresponding IDs currently playing in the English Premier League. You can use only those.
```
{teams}
```

You should reply only with the team ID. Don't add any more information.
"""

    def __init__(self, client: BedrockRuntimeClient):
        self._client = client

    def extract_team_id(self, query: str, teams: list[Team]) -> int:
        system_prompt = self._SYSTEM_PROMPT_TEMPLATE.format(
            teams=[{"name": team.name, "id": team.id} for team in teams]
        )

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self._MAX_TOKENS_TO_SAMPLE,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": query,
                            }
                        ],
                    }
                ],
            }
        )

        model_response = self._client.invoke_model(
            modelId=self._MODEL_ID,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        text_response = self._extract_text_response(model_response)

        return int(text_response)

    def _extract_text_response(self, model_response: InvokeModelResponseTypeDef) -> str:
        data: bytes = b""

        for event in model_response["body"]:
            data += event

        content = json.loads(data)["content"]
        text_response = "".join([entry["text"] for entry in content if entry["type"] == "text"])

        return text_response
