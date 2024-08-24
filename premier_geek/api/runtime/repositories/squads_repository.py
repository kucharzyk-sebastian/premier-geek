from typing import Any

import requests

from pydantic import BaseModel


POSITION_ID_TO_NAME = {
    24: "Goalkeeper",
    25: "Defender",
    26: "Midfielder",
    27: "Attacker",
    28: "Unknown",
    148: "Centre Back",
    149: "Defensive Midfield",
    150: "Attacking Midfield",
    151: "Centre Forward",
    152: "Left Wing",
    153: "Central Midfield",
    154: "Right Back",
    155: "Left Back",
    156: "Right Wing",
    157: "Left Midfield",
    158: "Right Midfield",
    163: "Secondary Striker",
    221: "Coach",
    226: "Assistant Coach",
    227: "Goalkeeping Coach",
    228: "Forward Coach",
    560: "Caretaker Manager",
}


class Player(BaseModel):
    first_name: str | None
    surname: str | None
    date_of_birth: str | None
    playing_position: str | None
    image_path: str | None


class SquadsRepository:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportmonks.com/v3/football/squads/teams"

    def get_squad(self, team_id: int) -> list[Player]:
        url = f"{self.base_url}/{team_id}/extended"
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": self.api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        squad_data: list[dict[str, Any]] = response.json()["data"]
        players: list[Player] = []

        for player_data in squad_data:
            player = Player(
                first_name=player_data["firstname"],
                surname=player_data["lastname"],
                date_of_birth=player_data.get("date_of_birth"),
                playing_position=POSITION_ID_TO_NAME.get(player_data["detailed_position_id"]),
                image_path=player_data.get("image_path"),
            )
            players.append(player)

        return players
