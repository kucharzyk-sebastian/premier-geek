import boto3

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from runtime.errors import UnrelatedQueryError
from runtime.repositories.squads_repository import Player
from runtime.repositories.squads_repository import SquadsRepository
from runtime.repositories.teams_repository import TeamsRepository
from runtime.security import verify_token
from runtime.services.team_id_extractor import TeamIdExtractor
from runtime.settings import Settings
from starlette import status


settings = Settings()

sports_monks_api_key = settings.sport_monks_api_key or ""

squads_repository = SquadsRepository(sports_monks_api_key)
teams_repository = TeamsRepository(sports_monks_api_key)
team_id_extractor = TeamIdExtractor(boto3.client(service_name="bedrock-runtime"))  # type: ignore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)


@app.exception_handler(UnrelatedQueryError)
async def value_error_exception_handler(request: Request, exc: UnrelatedQueryError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": "The question asked was unrelated."}
    )


@app.get("/players")
def get_players(query: str, authenticated: bool = Depends(verify_token)) -> list[Player]:
    teams = teams_repository.get_teams(season_id=23614)
    team_id = team_id_extractor.extract_team_id(query, teams)
    return squads_repository.get_squad(team_id=team_id)
