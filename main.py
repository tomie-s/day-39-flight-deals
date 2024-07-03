from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

origin_city_iata = "LON"

data_manager = DataManager()
google_sheet_data = data_manager.get_spreadsheet_data()
search = FlightSearch()
notification_manager = NotificationManager()


if google_sheet_data[0]["iataCode"] == "":
    for row in google_sheet_data:
        row['iataCode'] = search.get_destination_code(row['city'])

    data_manager.sheet_data = google_sheet_data
    data_manager.update_destination_code()

for row in google_sheet_data:
    print(f"Getting flights for {row['city']}...")
    results = search.check_flights(row, origin_city_iata)

    cheapest_flight = find_cheapest_flight(results)
    print(f"{row['city']}: £{cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < row['lowestPrice']:
        print(f"Lower price flight found to {row['city']}!")
        notification_manager.send_sms(
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_city_iata} to {cheapest_flight.destination_city}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
