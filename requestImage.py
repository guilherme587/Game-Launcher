import requests

class GameImageAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.rawg.io/api/games"

    def search_game_image(self, game_name):
        params = {"key": self.api_key, "search": game_name}
        response = requests.get(self.endpoint, params=params)
        response.raise_for_status()
        results = response.json()
        if results["results"]:
            return results["results"][0]["background_image"]
        return None
