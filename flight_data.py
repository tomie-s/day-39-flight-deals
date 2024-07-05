class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, price, origin_city, destination_city, out_date, return_date, stops):
        self.price = price
        self.origin_city = origin_city
        self.destination_city = destination_city
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(result):
    # Handle empty data if no flight or Amadeus rate limit exceeded
    if result is None or not result['data']:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    # Data from the first flight in the json
    first_flight = result['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
    stops = len(first_flight["itineraries"][0]["segments"]) - 1

    # Initialize FlightData with the first flight for comparison
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops)

    for flight in result["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            stops = len(first_flight["itineraries"][0]["segments"]) - 1
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops)
            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight
