import requests
import os
from datetime import date, timedelta

class Analizador:
    def __init__(self):
        self.api_key = os.getenv("API_FOOTBALL_KEY")
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        self.base_url = "https://v3.football.api-sports.io"

    def obtener_partidos(self, league_id, season="2026"):
        fecha_hoy = date.today().strftime("%Y-%m-%d")
        fecha_fin = date.today() + timedelta(days=3)

        url = f"{self.base_url}/fixtures"
        params = {"league": league_id, "season": season, "from": "2026-06-01", "to":"2026-06-30"}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            print(f"DEBUG: Status Code API: {response.status_code}")
            return response.json().get("response", [])
        except Exception as e:
            print(f"DEBUG: Error consultando API: {e}")
            return []