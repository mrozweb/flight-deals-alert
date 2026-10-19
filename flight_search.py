import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

SERP_ENDPOINT = os.getenv("ENV_SERP_ENDPOINT_GET")

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        # Serp API endpoint
        self._api_key = os.getenv("ENV_SERP_API_KEY")

        # Currency setting
        self.currency = os.getenv("ENV_CURRENCY", "EUR")

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        # Searches for flights between two cities using SerpAPI

        params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time,
            "return_date": to_time,
            "type": "1",
            "adults": "1",
            "currency": self.currency,
            "api_key": self._api_key,
        }

        # Only include stops parameter if is_direct is True
        if is_direct:
            params["stops"] = "0"

        response = requests.get(url=SERP_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        return data
