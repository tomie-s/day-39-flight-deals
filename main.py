from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

origin_city_iata = "LON"

data_manager = DataManager()
google_price_data = data_manager.get_price_data()
google_user_data = data_manager.get_customer_emails()
user_email_list = [user['email'] for user in google_user_data]
search = FlightSearch()
notification_manager = NotificationManager()

if google_price_data[0]["iataCode"] == "":
    for row in google_price_data:
        row['iataCode'] = search.get_destination_code(row['city'])

    data_manager.price_data = google_price_data
    data_manager.update_destination_code()

for row in google_price_data:
    print(f"Getting flights for {row['city']}...")
    direct_flights = search.check_flights(row, origin_city_iata)

    if direct_flights['meta']['count'] == 0:
        print(f"No direct flight to {row['city']}. Looking for indirect flights...")
        non_direct_flights = search.check_flights(row, origin_city_iata, is_direct=False)
        cheapest_flight = find_cheapest_flight(non_direct_flights)
    else:
        cheapest_flight = find_cheapest_flight(direct_flights)

    print(f"{row['city']}: £{cheapest_flight.price} with {cheapest_flight.stops} stops.")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < row['lowestPrice']:
        if cheapest_flight.stops == 0:
            email_message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct " \
                            f"from {cheapest_flight.origin_city} to {cheapest_flight.destination_city}, " \
                            f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            email_message = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                            f"from {cheapest_flight.origin_city} to {cheapest_flight.destination_city}, " \
                            f"with {cheapest_flight.stops} stop(s) " \
                            f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        notification_manager.send_emails(user_email_list, email_message)
