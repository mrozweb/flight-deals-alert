import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        # Initialize DataManager with credentials from .env

        # Sheety API endpoints
        self.SHEETY_ENDPOINT_GET = os.getenv("ENV_SHEETY_ENDPOINT_GET")
        self.SHEETY_ENDPOINT_PUT = os.getenv("ENV_SHEETY_ENDPOINT_PUT")
        self.SHEETY_ENDPOINT_POST = os.getenv("ENV_SHEETY_ENDPOINT_POST")
        self.SHEETY_AUTH = os.getenv("ENV_SHEETY_AUTH")

        # Headers for Sheety API
        self.headers = {
            "Authorization": self.SHEETY_AUTH,
            "Content-Type": "application/json",
        }

        # Currency setting
        self.currency = os.getenv("ENV_CURRENCY", "EUR")

        # Store the sheet data
        self.sheet_data = None

    def get_data(self):
        """
        READ all data from the spreadsheet (GET request)

        Returns:
            list: List of flight deal dictionaries
        """
        try:
            response = requests.get(
                url=self.SHEETY_ENDPOINT_GET,
                headers=self.headers
            )
            response.raise_for_status()

            # Direct access to "prices" key
            self.sheet_data = response.json()["prices"]

            print(f"Fetched {len(self.sheet_data)} rows from spreadsheet")
            return self.sheet_data

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data: {e}")
            return []

    def update_lowest_price(self, row_id, new_price):
        """
        Update the lowest price for a specific row in the spreadsheet (PUT request).

        Args:
            row_id (int): The ID of the row to update (from Sheety)
            new_price (int/float): The new lowest price to store

        Returns:
            dict: The updated row data from Sheety, or None if error
        """

        endpoint = f"{self.SHEETY_ENDPOINT_PUT}/{row_id}"

        update_spreadsheet = {
            "price": {
                "lowestPrice": new_price,
            }
        }

        try:
            response = requests.put(
                url=endpoint,
                json=update_spreadsheet,
                headers=self.headers,
            )
            response.raise_for_status()
            print(f"Updated lowest price for row {row_id} to {new_price:.0f}")
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error updating row {row_id}:, {e}")
            return None
