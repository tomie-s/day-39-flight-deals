import os
import requests


class DataManager:

    def __init__(self):
        self._user = os.environ['SHEETY_USERNAME']
        self._password = os.environ['SHEETY_PASSWORD']
        self.price_endpoint = os.environ['PRICE_ENDPOINT']
        self.user_endpoint = os.environ['USER_ENDPOINT']
        self.price_data = {}
        self.user_data = {}

    def get_price_data(self):
        response = requests.get(self.price_endpoint, auth=(self._user, self._password))
        response.raise_for_status()
        self.price_data = response.json()['prices']
        return self.price_data

    def update_destination_code(self):
        for row in self.price_data:
            update_endpoint = f"{self.price_endpoint}/{row['id']}"
            sheet_data = {
                "price": {
                    "iataCode": row['iataCode']
                }
            }
            response = requests.put(update_endpoint, auth=(self._user, self._password), json=sheet_data)
            response.raise_for_status()

    def get_customer_emails(self):
        response = requests.get(self.user_endpoint, auth=(self._user, self._password))
        response.raise_for_status()
        self.user_data = response.json()['users']
        return self.user_data
