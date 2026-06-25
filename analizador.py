import requests
import os
from datetime import date

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
        url = f"{self.base_url}/fixtures"
        params = {"date": fecha_hoy, "league": league_id, "season": season}
        response = requests.get(url, headers=self.headers, params=params).json()
        return response.get("response", [])
    
        params = {"date": fecha_hoy, "league": league_id, "season": season}
        
        try:
            response = requests.get(url, headers=self.headers, params=params).json()
            return response.get("response", [])
        except Exception as e:
            print(f"Error consultando API: {e}")
            return []