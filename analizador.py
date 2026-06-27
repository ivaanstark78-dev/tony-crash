import requests
import os

class Analizador:
    def __init__(self):
        self.api_key = os.getenv("FOOTBALL_DATA_TOKEN")
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        self.base_url = "https://api.football-data.org/v4"

    def obtener_partidos(self, league_id, season="2026"):
        url = f"{self.base_url}/fixtures"
        params = {
            "league": league_id, 
            "season": season, 
            "from": "2026-06-01", 
            "to": "2026-06-30"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            
            # Si la lista de partidos está vacía, enviamos el JSON crudo 
            # para depurar qué está pasando exactamente
            if not data.get("response"):
                return [{"error_debug": str(data)}]
                
            return data.get("response", [])
            
        except Exception as e:
            print(f"DEBUG: Error consultando API: {e}")
            return [{"error_debug": f"Error de conexión: {str(e)}"}]