import requests

from pydantic import BaseModel


class Team(BaseModel):
    id: int
    name: str


class TeamsRepository:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportmonks.com/v3/football/teams/seasons"

    def get_teams(self, season_id: int) -> list[Team]:
        url = f"{self.base_url}/{season_id}"
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": self.api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        teams_data = response.json()["data"]
        teams: list[Team] = []

        for team_data in teams_data:
            team = Team(id=team_data["id"], name=team_data["name"])
            teams.append(team)

        return teams
