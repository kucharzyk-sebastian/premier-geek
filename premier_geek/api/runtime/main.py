from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from runtime.repositories.squads_repository import Player
from runtime.repositories.squads_repository import SquadsRepository
from runtime.security import verify_token
from runtime.settings import Settings


settings = Settings()

sports_monks_api_key = settings.sport_monks_api_key or ""

squads_repository = SquadsRepository(sports_monks_api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)


@app.get("/players")
def get_players(authenticated: bool = Depends(verify_token)) -> list[Player]:
    return squads_repository.get_squad(14)
