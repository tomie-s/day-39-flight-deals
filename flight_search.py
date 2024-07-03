import os
import requests
from datetime import datetime, timedelta
from random import randint

DEPARTURE_DATE = datetime.now() + timedelta(randint(1, 180))
RETURN_DATE = DEPARTURE_DATE + timedelta(randint(3, 30))

FLIGHT_OFFERS_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"


class FlightSearch:

    def __init__(self):
        self._api_key = os.environ['AMADEUS_API_KEY']
        self._api_secret = os.environ['AMADEUS_API_SECRET']
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }

        response = requests.post(TOKEN_ENDPOINT, headers=header, data=body, verify=False)
        response.raise_for_status()

        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")

        return response.json()['access_token']

    def get_destination_code(self, city_name):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }

        response = requests.get(IATA_ENDPOINT, headers=headers, params=query)
        response.raise_for_status()

        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "IATA code not available"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "City name not found"

        return code

    def check_flights(self, city, origin_city):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city,
            "destinationLocationCode": city['iataCode'],
            "departureDate": DEPARTURE_DATE.strftime("%Y-%m-%d"),
            "returnDate": RETURN_DATE.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": 10
        }
        response = requests.get(FLIGHT_OFFERS_ENDPOINT, params=query, headers=headers)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()
