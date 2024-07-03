import os
import requests


class DataManager:

    def __init__(self):
        self._user = os.environ['SHEETY_USERNAME']
        self._password = os.environ['SHEETY_PASSWORD']
        self.sheet_data = {}

    def get_spreadsheet_data(self):
        sheety_endpoint = "https://api.sheety.co/69ea3f7eb3ff37bf7e48768326cded04/flightDeals/prices"

        response = requests.get(sheety_endpoint, auth=(self._user, self._password))
        response.raise_for_status()
        self.sheet_data = response.json()['prices']
        return self.sheet_data

    def update_destination_code(self):
        for row in self.sheet_data:
            update_endpoint = f"https://api.sheety.co/69ea3f7eb3ff37bf7e48768326cded04/flightDeals/prices/{row['id']}"
            sheet_data = {
                "price": {
                    "iataCode": row['iataCode']
                }
            }
            response = requests.put(update_endpoint, auth=(self._user, self._password), json=sheet_data)
            response.raise_for_status()
